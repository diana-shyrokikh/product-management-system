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
        db=db, order=order, user_id=user.id
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
