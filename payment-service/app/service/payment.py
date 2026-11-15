import asyncio
from uuid import uuid4

from aio_pika.abc import AbstractExchange
from app.config import settings
from app.rabbitmq import event_publish_json
from app.repository.payment import PaymentRepository
from app.schemas import PaymentCreateSchema, PaymentReadSchema
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


class PaymentService:
    async def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.payment_repository = PaymentRepository(db)

    async def get(self, payment_id: str) -> PaymentReadSchema:
        payment_orm = await self.payment_repository.get_one(payment_id)
        if not payment_orm:
            raise HTTPException(404, f"Payment id {payment_id} not found")

        return PaymentReadSchema.model_validate(payment_orm)

    async def create(self, payload: PaymentCreateSchema) -> PaymentReadSchema:
        payment_orm = await self.payment_repository.create(payload=payload)
        await self.db.commit()
        return PaymentReadSchema.model_validate(payment_orm)

    async def complete_payment(
        self,
        payment: PaymentReadSchema,
        exchange: AbstractExchange,
        user_id: str,
        amount: int,
        order_id: str,
    ) -> PaymentReadSchema:
        await asyncio.sleep(4)
        payment.status = "succeeded"

        await self.db.commit()

        event = {
            "order_id": order_id,
            "status": "succeeded",
            "amount": amount,
            "user_id": user_id,
            "event_id": str(uuid4),
        }
        await event_publish_json(
            exchange=exchange,
            routing_key=settings.payment_succeeded_routing_key,
            data=event,
        )

        return PaymentReadSchema.model_validate(payment)
