import re

from pydantic import BaseModel, field_validator


class CategoryBase(BaseModel):
    name: str


class CreateCategory(BaseModel):
    name: str

    @field_validator("name")
    def validate_name(cls, name):
        pattern = r"^[A-Za-z][A-Za-z0-9\s]*$"

        if not re.match(pattern, name):
            raise ValueError(
                "Name must only contain letters, "
                "numbers, or spaces"
            )

        return name


class UpdateCategory(BaseModel):
    name: str = None

    @field_validator("name")
    def validate_name(cls, name):
        if name is not None:
            pattern = r"^[A-Za-z][A-Za-z0-9\s]*$"

            if not re.match(pattern, name):
                raise ValueError(
                    "Name must only contain letters, "
                    "numbers, or spaces"
                )

            return name


class Category(CategoryBase):
    id: int

    class Config:
        orm_mode: True


class DeleteCategory(BaseModel):
    message: str
