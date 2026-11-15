from app.api.dependencies import get_payment_service
from app.schemas import PaymentCreateSchema, PaymentReadSchema
from app.service.payment import PaymentService
from fastapi import APIRouter, Depends, Request

router = APIRouter()


@router.get("/payment/{payment_id}")
async def get_payment(
    payment_id: str, payment_service: PaymentService = Depends(get_payment_service)
) -> PaymentReadSchema:
    return await payment_service.get(payment_id)


@router.post("/payment")
async def create_payment(
    payload: PaymentCreateSchema,
    request: Request,
    payment_service: PaymentService = Depends(get_payment_service),
) -> PaymentReadSchema:
    payment = await payment_service.create(payload)
    return await payment_service.complete_payment(
        payment=payment,
        exchange=request.app.state.payment_exchange,
        user_id=payload.user_id,
        amount=payload.amount,
        order_id=payload.order_id,
    )
