from app.clients import CatalogClient, PaymentClient
from app.repository.order import CatalogRepository
from app.schemas import OrderCreateSchema, OrderReadSchema
from fastapi import HTTPException
from sqlalchemy.orm import Session


class OrderService:
    def __init__(
        self, db: Session, catalog_client: CatalogClient, payment_client: PaymentClient
    ) -> None:
        self.db = db
        self.catalog_repository = CatalogRepository(db)
        self.catalog_client = catalog_client
        self.payment_client = payment_client

    def get(self, order_id: str) -> OrderReadSchema:
        order_orm = self.catalog_repository.get_one(order_id)
        if not order_orm:
            raise HTTPException(404, f"Order id {order_id} not found")

        return OrderReadSchema.model_validate(order_orm)

    def create(self, payload: OrderCreateSchema) -> OrderReadSchema:

        products = []
        for item in payload.items:
            product = self.catalog_client.get_product(item.product_id)
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
        order_orm = self.catalog_repository.create(
            payload=payload, total_amount=total_amount, products=products
        )
        self.db.commit()
        self.payment_client.create_payment(
            order_id=order_orm.id, user_id=order_orm.user_id, amount=total_amount
        )

        return OrderReadSchema.model_validate(order_orm)
