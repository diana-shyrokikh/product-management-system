from pydantic import BaseModel

import products.schemas


class CreateOrder(BaseModel):
    products: list[products.schemas.OrderProduct]


class PendingOrder(BaseModel):
    id: int
    products: list[products.schemas.BuyProduct]
    status: str
    total_price: float
    payment_url: str
    message: str = (
        "Order details were also sent to your email. "
        "The order will be deleted in case payment cancelling"
    )


class Message(BaseModel):
    message: str
