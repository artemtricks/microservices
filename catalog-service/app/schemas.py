from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str
    category: str
    image: str
    price: int


class ProductRead(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    name: str
    description: str
    category: str
    image: str
    price: int
