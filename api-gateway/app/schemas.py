from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CreadentialsBase(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserRegister(CreadentialsBase):
    pass


class UserLogin(CreadentialsBase):
    pass


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: EmailStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead


class ProductRead(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    name: str
    description: str
    category: str
    image: str
    price: int


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
    total_amount: int
    status: str
    items: list[OrderItemReadSchema]
