from fastapi import FastAPI

from products import router as product_router
from product_categories import router as category_router
from users import router as user_router

app = FastAPI()

app.include_router(product_router.router)
app.include_router(category_router.router)
app.include_router(user_router.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
