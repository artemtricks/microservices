import asyncio

from app.models import PaymentOrm
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

    async def complete_payment(self, payment: PaymentOrm):
        await asyncio.sleep(4)
        payment.status = "succeeded"

        await self.db.commit()
        await event_publish_json()
