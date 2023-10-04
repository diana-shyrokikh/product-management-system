from passlib.context import CryptContext
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from users import models, schemas


async def get_all_users(
        db: AsyncSession,
) -> list[models.User]:
    query = select(models.User)
    user_list = await db.execute(query)
    return [
        user[0]
        for user
        in user_list.fetchall()
    ]


async def get_user(
        db: AsyncSession,
        user_id: int
) -> [models.User | None]:
    query = select(models.User).where(
        models.User.id == user_id
    )
    user = await db.execute(query)
    user = user.fetchone()

    if user:
        return user[0]

    return None


async def get_user_by_username(
        db: AsyncSession,
        user_username: str
) -> [models.User | None]:
    query = select(models.User).where(
        models.User.username == user_username
    )
    user = await db.execute(query)
    user = user.fetchone()

    if user:
        return user[0]

    return None


async def create_user(
        db: AsyncSession,
        user: schemas.CreateUser
) -> dict:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    user.username = user.username.strip()
    user.email = user.email.strip()
    user.password = pwd_context.hash(user.password.strip())

    query = insert(models.User).values(
        username=user.username,
        email=user.email,
        phone_number=user.phone_number,
        password=user.password,
    )

    new_user = await db.execute(query)

    await db.commit()

    new_user = {
        **user.model_dump(),
        "id": new_user.lastrowid,
    }

    return new_user


async def update_user(
        db: AsyncSession,
        user_id: int,
        new_data: schemas.UpdateUser,
) -> [models.User | None]:
    query = select(models.User).where(
        models.User.id == user_id
    )
    updated_user = await db.execute(query)
    updated_user = updated_user.fetchone()

    if updated_user:
        updated_user = updated_user[0]

        if new_data.username:
            updated_user.username = new_data.username.strip()
        if new_data.email:
            updated_user.email = new_data.email.strip()
        if new_data.phone_number:
            updated_user.phone_number = new_data.phone_number
        if new_data.password:
            pwd_context = CryptContext(
                schemes=["bcrypt"], deprecated="auto"
            )
            updated_user.password = pwd_context.hash(new_data.password)

        await db.commit()
        await db.refresh(updated_user)

        return updated_user

    return None


async def delete_user(
        db: AsyncSession,
        user_id: int,
) -> [dict | bool]:
    query = select(models.User).where(
        models.User.id == user_id
    )
    deleted_user = await db.execute(query)
    deleted_user = deleted_user.fetchone()

    if deleted_user:
        await db.delete(deleted_user[0])
        await db.commit()

        return {"message": "User deleted"}

    return False
