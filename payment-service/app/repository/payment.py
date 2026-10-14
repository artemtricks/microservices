from app.models import PaymentOrm
from app.schemas import PaymentCreateSchema
from sqlalchemy.ext.asyncio import AsyncSession


class PaymentRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_one(self, payment_id: str) -> PaymentOrm | None:
        return await self.db.get(PaymentOrm, payment_id)

    async def create(self, payload: PaymentCreateSchema) -> PaymentOrm:
        new_payment = PaymentOrm(
            order_id=payload.order_id, status="created", amount=payload.amount
        )
        self.db.add(new_payment)

        return new_payment
