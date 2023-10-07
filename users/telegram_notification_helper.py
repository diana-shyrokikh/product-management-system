import os

from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")


async def send_telegram_order_detail(
    order: dict,
    phone_number: str
) -> None:
    products = make_products_msg(order.get("products"))
    order_detail = f"""
    This is your order detail
    Total price: {order.get("total_price")}$
    Products: {products}
    Link to pay: 
    {order.get("payment_url")}
    """
    try:
        async with TelegramClient(
                "user_session", int(API_ID), API_HASH
        ) as client:
            await client.send_message(phone_number, order_detail)

    except Exception:
        pass


def make_products_msg(products: list) -> str:
    products_msg = """"""

    for product in products:
        products_msg += f"""
        {product.get("name")}
        Price: {product.get("price")}$
        Quantity: {product.get("quantity")}
        """

    return products_msg
