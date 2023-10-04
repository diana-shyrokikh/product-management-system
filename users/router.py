from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import (
    get_db,
    common_object_parameters,
)

from users import crud, schemas


router = APIRouter()


@router.get(
    "/users/",
    response_model=list[schemas.User],
)
async def read_users(
    db: AsyncSession = Depends(get_db),
) -> [list[schemas.User] | list]:
    return await crud.get_all_users(db=db)


@router.get(
    "/users/{user_id}/",
    response_model=schemas.User,
)
async def retrieve_user(
    commons: Annotated[
        dict, Depends(common_object_parameters)
    ],
) -> [schemas.User | Exception]:
    user = await crud.get_user(
        db=commons.get("db"),
        user_id=commons.get("object_id")
    )

    if user:
        return user

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )


@router.post(
    "/users/",
    response_model=schemas.User,
)
async def create_user(
    user: schemas.CreateUser,
    db: AsyncSession = Depends(get_db),
) -> [schemas.User | Exception]:
    if await crud.get_user_by_username(
            db=db, user_username=user.username
    ):
        raise HTTPException(
            status_code=400,
            detail="Such user already exist"
        )

    return await crud.create_user(db=db, user=user)


@router.put(
    "/users/{user_id}/",
    response_model=schemas.User,
)
async def update_user(
    commons: Annotated[
        dict, Depends(common_object_parameters)
    ],
    new_data: schemas.UpdateUser,
) -> [schemas.User | Exception]:
    updated_user = await crud.update_user(
        db=commons.get("db"),
        user_id=commons.get("object_id"),
        new_data=new_data,
    )

    if updated_user:
        return updated_user

    raise HTTPException(
        status_code=404,
        detail="You cannot update user data which not found"
    )


@router.delete(
    "/users/{user_id}/",
    response_model=schemas.DeleteUser,
)
async def delete_user(
    commons: Annotated[
        dict, Depends(common_object_parameters)
    ],
) -> [schemas.DeleteUser | Exception]:
    deleted_user = await crud.delete_user(
        db=commons.get("db"),
        user_id=commons.get("object_id"),
    )

    if deleted_user:
        return deleted_user

    raise HTTPException(
        status_code=404,
        detail="You cannot delete the user which not found"
    )
