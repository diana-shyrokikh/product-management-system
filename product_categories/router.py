from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import (
    get_db,
    common_object_parameters,
)

from product_categories import crud, schemas

router = APIRouter()


@router.get(
    "/categories/",
    response_model=list[schemas.Category],
)
async def read_categories(
    db: AsyncSession = Depends(get_db),
) -> [list[schemas.Category] | list]:
    return await crud.get_all_categories(db=db)


@router.get(
    "/categories/{category_id}/",
    response_model=schemas.Category,
)
async def retrieve_category(
    commons: Annotated[
        dict, Depends(common_object_parameters)
    ],
) -> [schemas.Category | Exception]:
    category = await crud.get_category(
        db=commons.get("db"),
        category_id=commons.get("object_id")
    )

    if category:
        return category

    raise HTTPException(
        status_code=404,
        detail="Category not found"
    )


@router.post(
    "/categories/",
    response_model=schemas.Category,
)
async def create_category(
    category: schemas.CreateCategory,
    db: AsyncSession = Depends(get_db),
) -> [schemas.Category | Exception]:
    if await crud.get_category_by_name(
            db=db, category_name=category.name
    ):
        raise HTTPException(
            status_code=400,
            detail="Such category already exists"
        )

    return await crud.create_category(db=db, category=category)


@router.put(
    "/categories/{category_id}/",
    response_model=schemas.Category,
)
async def update_category(
    commons: Annotated[
        dict, Depends(common_object_parameters)
    ],
    new_data: schemas.UpdateCategory,
) -> [schemas.Category | Exception]:
    updated_category = await crud.update_category(
        db=commons.get("db"),
        category_id=commons.get("object_id"),
        new_data=new_data,
    )

    if updated_category:
        return updated_category

    raise HTTPException(
        status_code=404,
        detail="You cannot update category data which not found"
    )


@router.delete(
    "/categories/{category_id}/",
    response_model=schemas.DeleteCategory,
)
async def delete_category(
    commons: Annotated[
        dict, Depends(common_object_parameters)
    ],
) -> [schemas.DeleteCategory | Exception]:
    deleted_category = await crud.delete_category(
        db=commons.get("db"),
        category_id=commons.get("object_id"),
    )

    if deleted_category:
        return deleted_category

    raise HTTPException(
        status_code=404,
        detail="You cannot delete the category which not found"
    )
