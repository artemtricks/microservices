from app.api_clients import request_service
from app.auth import CurrentUser, get_current_user
from app.config import settings
from app.schemas import OrderCreateSchema, OrderReadSchema
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/orders", tags=["order"])


@router.get("/{order_id}")
async def get_order(
    order_id: str,
    current_user=Depends(get_current_user),
) -> OrderReadSchema:
    order = await request_service(
        method="GET", url=f"{settings.ORDER_SERVICE_URL}/order/{order_id}"
    )
    ensure_order_owner(order=order, user=current_user)
    return order


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(
    payload: OrderCreateSchema,
    current_user=Depends(get_current_user),
) -> OrderReadSchema:

    order_payload = payload.model_dump(mode="json")
    order_payload["user_id"] = current_user.id
    return await request_service(
        method="POST",
        url=f"{settings.ORDER_SERVICE_URL}/order",
        json_body=order_payload,
    )


def ensure_order_owner(order, user: CurrentUser) -> None:
    if not isinstance(order, dict) or order.get("user_id") != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
