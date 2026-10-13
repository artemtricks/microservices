from pydantic import BaseModel, ConfigDict






    

class PaymentReadSchema(BaseModel):
    model_config = {'from_attributes': True}

    id:str
    order_id: str
    user_id: str
    amount: str
   
class PaymentCreateSchema(BaseModel):
   
    order_id: str
    user_id: str
    amount: str

