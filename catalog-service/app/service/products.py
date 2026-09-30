from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas import ProductRead as ProductReadeSchema, ProductCreate as ProductCreateSchema
from app.repository.products import ProductsRepository


class ProductsService:
    def __init__(self, db: Session) -> None:
        self.db = db;
        self.product_repository = ProductsRepository(db)


    def list_products(self) -> list[ProductReadeSchema]:
        products_orm = self.product_repository.get_all()
        products_read = [ProductReadeSchema.model_validate(product) for product in products_orm]
        return products_read


    def get_one_product(self, product_id: str) -> ProductReadeSchema:
        product_orm = self.product_repository.get_one(product_id)

        if not product_orm:
                 raise HTTPException(404, f'Prodct id {product_id} not found')
        
        return ProductReadeSchema.model_validate(product_orm)
        

    def create_product(self,  payload: ProductCreateSchema) -> ProductReadeSchema:
        new_product = self.product_repository.create(payload)
        self.db.commit()
        return ProductReadeSchema.model_validate(new_product)
