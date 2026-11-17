from datetime import datetime

from pydantic import BaseModel


class NotificationReadSchema(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    order_id: str
    user_id: str
    message: str
    is_read: bool
    created_at: datetime


class NotificationCreateSchema(BaseModel):
    order_id: str
    user_id: str
    message: str
