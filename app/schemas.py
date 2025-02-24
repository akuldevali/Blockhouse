from pydantic import BaseModel

class OrderBase(BaseModel):
    symbol: str
    price: float
    quantity: float
    order_type: str

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int

    class Config:
        orm_mode = True
