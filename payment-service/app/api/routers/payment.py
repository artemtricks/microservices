from fastapi import APIRouter, Depends
from app.schemas import PaymentCreateSchema, PaymentReadSchema
from app.service.payment import PaymentService
from app.api.dependencies import get_payment_service


router = APIRouter()


@router.get('/payment/{payment_id}')
def get_payment(payment_id: str, payment_service: PaymentService = Depends(get_payment_service)) -> PaymentReadSchema:
    return payment_service.get(payment_id)


@router.post('/payment')
def create_payment(payload: PaymentCreateSchema, payment_service: PaymentService = Depends(get_payment_service)) -> PaymentReadSchema:
    return payment_service.create(payload)