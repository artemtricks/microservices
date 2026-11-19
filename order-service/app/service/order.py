from app.clients import CatalogClient, PaymentClient
from app.messaging import build_order_paid_event
from app.repository.order import OrderRepository
from app.schemas import OrderCreateSchema, OrderReadSchema
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


class OrderService:
    def __init__(
        self,
        db: AsyncSession,
        catalog_client: CatalogClient,
        payment_client: PaymentClient,
    ) -> None:
        self.db = db
        self.order_repository = OrderRepository(db)
        self.catalog_client = catalog_client
        self.payment_client = payment_client

    async def get_all(self) -> list[OrderReadSchema]:
        orders_orm = await self.order_repository.get_all()
        orders_read = [OrderReadSchema.model_validate(order) for order in orders_orm]
        return orders_read

    async def get(self, order_id: str) -> OrderReadSchema:
        order_orm = await self.order_repository.get_one(order_id)
        if not order_orm:
            raise HTTPException(404, f"Order id {order_id} not found")

        return OrderReadSchema.model_validate(order_orm)

    async def create(self, payload: OrderCreateSchema) -> OrderReadSchema:

        products = []
        for item in payload.items:
            product = await self.catalog_client.get_product(item.product_id)
            products.append(
                {
                    "product_id": product["id"],
                    "product_name": product["name"],
                    "quantity": item.quantity,
                    "unit_price": product["price"],
                }
            )
        total_amount = sum(
            product["unit_price"] * product["quantity"] for product in products
        )
        order_orm = await self.order_repository.create(
            payload=payload, total_amount=total_amount, products=products
        )
        order_id = order_orm.id
        user_id = order_orm.user_id

        await self.db.commit()
        await self.payment_client.create_payment(
            order_id=order_id, user_id=user_id, amount=total_amount
        )

        return OrderReadSchema.model_validate(order_orm)

    async def handle_payment_succeeded(self, event: dict):
        order = await self.order_repository.get_one(event["order_id"])
        if order is None:
            raise ValueError("Order not found")
        if order.status == "paid":
            return
        order.status = "paid"
        await self.db.commit()

        return build_order_paid_event(user_id=order.user_id, order_id=order.id)
