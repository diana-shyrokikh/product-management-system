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
    is_admin,
)

from users import crud, schemas, utils
from users.utils import verify_token

router = APIRouter()


@router.get(
    "/users/",
    response_model=list[schemas.User],
)
async def read_users(
    db: AsyncSession = Depends(get_db),
    admin: schemas.User = Depends(is_admin)
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
    admin: schemas.User = Depends(is_admin)
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
            status_code=400,
            detail="Such user already exist"
        )

    return await crud.create_user(db=db, user=user)


@router.put(
    "/me/",
    response_model=schemas.User,
)
async def update_user(
    new_data: schemas.UpdateUser,
    db: AsyncSession = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
) -> [schemas.User | Exception]:
    return await crud.update_user(
        db=db,
        user=user,
        new_data=new_data
    )


@router.delete(
    "/users/{user_id}/",
    response_model=schemas.DeleteUser,
)
async def delete_user(
    commons: Annotated[
        dict, Depends(common_object_parameters)
    ],
    admin: schemas.User = Depends(is_admin)
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


@router.post("/login/", response_model=schemas.Token)
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


@router.post("/refresh_token/", response_model=schemas.Token)
async def refresh_token(
    token: str,
) -> [schemas.Token | Exception]:
    payload = verify_token(token=token, token_type="refresh")
    new_access_token = utils.create_token(
        payload.get("sub"),
        "refresh",
    )

    return {
        "access_token": new_access_token,
        "refresh_token": token
    }


@router.get("/me/",  response_model=schemas.User)
async def get_my_profile(
        user: schemas.User = Depends(get_current_user)
) -> [schemas.User | Exception]:
    return user
