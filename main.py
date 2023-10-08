from fastapi import FastAPI

from products import router as product_router
from product_categories import router as category_router
from users import router as user_router
from orders import router as order_router


app = FastAPI()

app.include_router(product_router.router)
app.include_router(category_router.router)
app.include_router(user_router.router)
app.include_router(order_router.router)


@app.get("/")
async def root():
    return {
        "greeting":
            "Hello from ProductManagementAPI! "
            "Here is the short route list :)",

        "/docs/": "Documentation",

        "/signup/": "Make registration on the API",
        "/login/": "Login on the API",
        "/refresh_token/": "Update your access token",
        "/me/": "Your profile",

        "/products/": "All products",
        "/products/product_id": "Get the product info by id",

        "/categories": "All categories",
        "/categories/category_id": "Get the category info by id",

        "/orders/": "Make an order",
    }
