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
    is_admin,
)

from orders import crud, schemas

from users import schemas as user_schemas

router = APIRouter()


@router.get(
    "/orders/",
    response_model=list[schemas.Order],
)
async def get_all_orders(
    db: AsyncSession = Depends(get_db),
    admin: user_schemas.User = Depends(is_admin)
) -> list[dict]:
    return await crud.get_all_orders(db=db)


@router.get(
    "/orders/{object_id}/",
    response_model=schemas.Order,
)
async def get_order(
    commons: Annotated[
        dict, Depends(common_object_parameters)
    ],
    admin: user_schemas.User = Depends(is_admin)
) -> [schemas.Order | Exception]:
    order = await crud.get_order(
        db=commons.get("db"), order_id=commons.get("object_id")
    )

    if order:
        return order

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Order not found"
    )


@router.post(
    "/order/",
    response_model=schemas.PendingOrder,
)
async def create_order(
    order: schemas.CreateOrder,
    db: AsyncSession = Depends(get_db),
    user: user_schemas.User = Depends(get_current_user)
) -> [schemas.PendingOrder | Exception]:
    order = await crud.create_order(
        db=db,
        order=order,
        user_id=user.id,
        username=user.username,
        user_email=user.email,
        user_phone=user.phone_number
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
