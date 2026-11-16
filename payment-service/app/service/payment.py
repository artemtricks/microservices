import asyncio

from aio_pika.abc import AbstractExchange
from app.config import settings
from app.events import build_payment_succeeded_event
from app.models import PaymentOrm
from app.rabbitmq import event_publish_json
from app.repository.payment import PaymentRepository
from app.schemas import PaymentCreateSchema, PaymentReadSchema
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


class PaymentService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.payment_repository = PaymentRepository(db)

    async def get_all(
        self,
    ) -> list[PaymentReadSchema]:
        payments_orm = await self.payment_repository.get_all()
        return [PaymentReadSchema.model_validate(payment) for payment in payments_orm]

    async def get(self, payment_id: str) -> PaymentReadSchema:
        payment_orm = await self.payment_repository.get_one(payment_id)
        if not payment_orm:
            raise HTTPException(404, f"Payment id {payment_id} not found")

        return PaymentReadSchema.model_validate(payment_orm)

    async def create(self, payload: PaymentCreateSchema) -> PaymentOrm:
        payment_orm = await self.payment_repository.create(payload=payload)
        await self.db.commit()
        return payment_orm

    async def complete_payment(
        self,
        payment: PaymentOrm,
        exchange: AbstractExchange,
        amount: int,
        order_id: str,
    ) -> PaymentReadSchema:
        await asyncio.sleep(4)
        payment.status = "succeeded"

        await self.db.commit()

        event = build_payment_succeeded_event(
            payment_id=payment.id, order_id=order_id, amount=amount
        )
        await event_publish_json(
            exchange=exchange,
            routing_key=settings.payment_succeeded_routing_key,
            data=event,
        )

        return PaymentReadSchema.model_validate(payment)
