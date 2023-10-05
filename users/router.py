from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import (
    get_db,
    common_object_parameters,
    get_current_user,
)

from users import crud, schemas, utils

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
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )


@router.post(
    "/signup/",
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
            status_code=status.HTTP_400_BAD_REQUEST,
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
        status_code=status.HTTP_404_NOT_FOUND,
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
        status_code=status.HTTP_404_NOT_FOUND,
        detail="You cannot delete the user which not found"
    )


@router.post("/login", response_model=schemas.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> [schemas.Token | Exception]:
    tokens = await crud.login_user(
        db, form_data.username, form_data.password
    )

    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )

    return tokens


@router.post("/refresh_token", response_model=schemas.Token)
async def refresh_token(
    token: str,
) -> [schemas.Token | Exception]:
    user = await get_current_user(token=token, token_type="refresh")
    new_access_token = utils.create_token(
        user,
        "refresh",
    )

    return {
        "access_token": new_access_token,
        "refresh_token": token
    }


@router.get("/me",  response_model=schemas.User)
async def get_me(
        user: schemas.User = Depends(get_current_user)
) -> [schemas.User | Exception]:
    return user
