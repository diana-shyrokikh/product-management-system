from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import (
    get_db,
    common_product_parameters,
)

from products import crud, schemas


router = APIRouter()


@router.get(
    "/products/",
    response_model=list[schemas.Product],
)
async def read_products(
    db: AsyncSession = Depends(get_db),
) -> [list[schemas.Product] | list]:
    return await crud.get_all_products(db=db)


@router.get(
    "/products/{product_id}/",
    response_model=schemas.Product,
)
async def retrieve_product(
    commons: Annotated[
        dict, Depends(common_product_parameters)
    ],
) -> [schemas.Product | Exception]:
    product = await crud.get_product(
        db=commons.get("db"),
        product_id=commons.get("product_id")
    )

    if product:
        return product

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )


@router.post(
    "/products/",
    response_model=schemas.Product,
)
async def create_product(
    product: schemas.CreateProduct,
    db: AsyncSession = Depends(get_db),
) -> [schemas.Product | Exception]:
    if await crud.get_product_by_name(
            db=db, product_name=product.name
    ):
        raise HTTPException(
            status_code=400,
            detail="Such product already exists"
        )

    return await crud.create_product(db=db, product=product)


@router.put(
    "/products/{product_id}/",
    response_model=schemas.Product,
)
async def update_product(
    commons: Annotated[
        dict, Depends(common_product_parameters)
    ],
    new_data:  dict,
) -> [schemas.Product | Exception]:
    updated_product = await crud.update_product(
        db=commons.get("db"),
        product_id=commons.get("product_id"),
        new_data=new_data,
    )

    if updated_product:
        return updated_product

    raise HTTPException(
        status_code=404,
        detail="You cannot update product data which not found"
    )


@router.delete(
    "/products/{product_id}/",
    response_model=schemas.DeleteProduct,
)
async def delete_product(
    commons: Annotated[
        dict, Depends(common_product_parameters)
    ],
) -> [schemas.DeleteProduct | Exception]:
    deleted_product = await crud.delete_product(
        db=commons.get("db"),
        product_id=commons.get("product_id"),
    )

    if deleted_product:
        return deleted_product

    raise HTTPException(
        status_code=404,
        detail="You cannot delete the product which not found"
    )
