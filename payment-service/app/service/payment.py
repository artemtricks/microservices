from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repository.payment import PaymentRepository
from app.schemas import PaymentReadSchema, PaymentCreateSchema




class PaymentService():
    def __init__(self, db: Session) -> None:
        self.db = db
        self.payment_repository = PaymentRepository(db)
       

    def get(self, payment_id: str) -> PaymentReadSchema:
        payment_orm = self.payment_repository.get_one(payment_id)
        if not payment_orm:
            raise HTTPException(404, f'Payment id {payment_id} not found')
        
        return PaymentReadSchema.model_validate(payment_orm)

    
    def create(self, payload: PaymentCreateSchema) -> PaymentReadSchema:
        payment_orm = self.payment_repository.create(payload=payload)
        self.db.commit()
        return PaymentReadSchema.model_validate(payment_orm)
        




        