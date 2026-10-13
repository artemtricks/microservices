from sqlalchemy.orm import Session
from app.models import PaymentOrm
from app.schemas import PaymentReadSchema, PaymentCreateSchema


class PaymentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_one(self, payment_id: str) -> PaymentOrm | None:
        return self.db.get(PaymentOrm, payment_id)

    def  create(self, payload: PaymentCreateSchema) -> PaymentOrm:
        new_payment = PaymentOrm(order_id=payload.order_id, status='created', amount=payload.amount)
        self.db.add(new_payment)
        
        return new_payment

