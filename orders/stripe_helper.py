import os

import stripe
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


def create_stripe_session(
    total_price,
    username,
    order_id,
):
    one_dollar_in_cents = 100
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "unit_amount":
                    int(total_price * one_dollar_in_cents),
                "product_data": {
                    "name": f"ProductManagerAPI Order",
                    "description": f"User: {username}",
                },
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=f"http://localhost:8000/success/{order_id}/",
        cancel_url=f"http://localhost:8000/cancel/{order_id}/",
    )

    return session.url
