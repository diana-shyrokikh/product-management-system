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
        "The order will be deleted "
        "if you close the page before making payment "
        "or in case payment canceling"
    )


class Message(BaseModel):
    message: str
