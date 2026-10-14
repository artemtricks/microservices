from app.models import Product
from app.schemas import ProductCreate as ProductCreateSchema
from sqlalchemy.orm import Session


class ProductsRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[Product]:
        return self.db.query(Product).all()

    def get_one(self, product_id: str) -> Product | None:
        return self.db.get(Product, product_id)

    def create(self, payload: ProductCreateSchema) -> Product | None:
        new_product = Product(
            name=payload.name,
            category=payload.category,
            price=payload.price,
            description=payload.description,
            image=payload.image,
        )
        self.db.add(new_product)
        return new_product
