from app.models import Order, OrderItem
from app.schemas import OrderCreateSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class OrderRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all(self) -> list[Order]:
        # result = await self.db.scalars(select(Order))
        # return list(result.all())
        result = await self.db.execute(select(Order).options(selectinload(Order.items)))
        orders_orm = result.scalars().all()
        return list(orders_orm)

    async def get_one(self, order_id: str) -> Order | None:
        result = await self.db.execute(
            select(Order).options(selectinload(Order.items)).where(Order.id == order_id)
        )
        return result.scalar_one_or_none()

    async def create(
        self, payload: OrderCreateSchema, total_amount: int, products: list
    ) -> Order:
        new_order = Order(
            user_id=payload.user_id, status="created", total_amount=total_amount
        )
        self.db.add(new_order)
        await self.db.flush()
        await self.db.refresh(new_order, attribute_names=["items"])
        new_order.items = [
            OrderItem(order_id=new_order.id, **product) for product in products
        ]

        return new_order
