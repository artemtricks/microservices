from app.api.dependencies import get_order_service
from app.schemas import OrderCreateSchema, OrderReadSchema
from app.service.order import OrderService
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/orders")
def get_all_orders(
    order_service: OrderService = Depends(get_order_service),
) -> list[OrderReadSchema]:
    return order_service.get_all()


@router.get("/order/{order_id}")
def get_order(
    order_id: str, order_service: OrderService = Depends(get_order_service)
) -> OrderReadSchema:
    return order_service.get(order_id)


@router.post("/order")
def create_order(
    payload: OrderCreateSchema, order_service: OrderService = Depends(get_order_service)
) -> OrderReadSchema:
    return order_service.create(payload)
