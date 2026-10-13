from sqlalchemy.orm import Session
from app.models import Order, OrderItem
from app.schemas import OrderCreateSchema, OrderItemCreateSchema, OrderItemReadSchema


class CatalogRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_one(self, order_id: str) -> Order | None:
        return self.db.get(Order, order_id)

    def  create(self, payload: OrderCreateSchema, total_amount: int, products: list) -> Order:
        new_order = Order(user_id=payload.user_id, status='created', total_amount=total_amount)
        self.db.add(new_order)
        self.db.flush()
        new_order.items = [OrderItem(order_id=new_order.id, **product) for product in products]

        return new_order

