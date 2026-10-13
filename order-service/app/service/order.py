from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repository.order import CatalogRepository
from app.schemas import OrderReadSchema, OrderCreateSchema
from clients.catalog_client import CatalogClient



class OrderService():
    def __init__(self, db: Session, catalog_client: CatalogClient) -> None:
        self.db = db
        self.catalog_repository = CatalogRepository(db)
        self.catalog_client = catalog_client

    def get(self, order_id: str) -> OrderReadSchema:
        order_orm = self.catalog_repository.get_one(order_id)
        if not order_orm:
            raise HTTPException(404, f'Order id {order_id} not found')
        
        return OrderReadSchema.model_validate(order_orm)

    
    def create(self, payload: OrderCreateSchema) -> OrderReadSchema:
        
        products = []
        for item in payload.items:
            product = self.catalog_client.get_product(item.product_id)
            products.append({
                'product_id': product['id'],
                'product_name': product['name'],
                'quantity': item.quantity,
                'unit_price': product['price']
            })
        total_amount = [product['unit_price'] for product in products]
        order_orm = self.catalog_repository.create(payload=payload, total_amount=total_amount, products=products)
        self.db.commit()
        return OrderReadSchema.model_validate(order_orm)
        




        