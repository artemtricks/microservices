from pydantic import BaseModel


class OrderCreateSchema(BaseModel):
    model_config = {"from_attributes": True}

    user_id: str
    items: list[OrderItemCreateSchema]  # noqa: F821


class OrderItemReadSchema(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    product_id: str
    product_name: str
    quantity: int
    unit_price: int


class OrderItemCreateSchema(BaseModel):
    product_id: str
    quantity: int


class OrderReadSchema(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    user_id: str
    total_amount: str
    status: str
    items: list[OrderItemReadSchema]
