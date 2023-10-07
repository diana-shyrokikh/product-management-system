from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import (
    get_db,
    get_current_user,
    common_object_parameters,
)

from orders import crud, schemas

from users import schemas as user_schema

router = APIRouter()


@router.post(
    "/order/",
    response_model=schemas.PendingOrder,
)
async def create_order(
    order: schemas.CreateOrder,
    db: AsyncSession = Depends(get_db),
    user: user_schema.User = Depends(get_current_user)
) -> [schemas.PendingOrder | Exception]:
    order = await crud.create_order(
        db=db,
        order=order,
        user_id=user.id,
        username=user.username,
        user_email=user.email
    )

    if order == status.HTTP_404_NOT_FOUND:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Such product doesn't exist"
        )
    if order == status.HTTP_406_NOT_ACCEPTABLE:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Not enough product quantity"
        )

    return order


@router.get(
    "/success/{object_id}/",
    response_model=schemas.Message
)
async def success(
    commons: Annotated[
        dict, Depends(common_object_parameters)
    ],
):
    return await crud.update_or_delete_order(
        db=commons.get("db"),
        order_id=commons.get("object_id"),
        order_status="paid"
    )


@router.get(
    "/cancel/{object_id}/",
    response_model=schemas.Message
)
async def cancel(
    commons: Annotated[
        dict, Depends(common_object_parameters)
    ],
):
    return await crud.update_or_delete_order(
        db=commons.get("db"),
        order_id=commons.get("object_id"),
        order_status="pending"
    )
