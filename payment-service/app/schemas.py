from pydantic import BaseModel


class PaymentReadSchema(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    order_id: str
    user_id: str
    amount: int
    status: str


class PaymentCreateSchema(BaseModel):
    order_id: str
    user_id: str
    amount: int
