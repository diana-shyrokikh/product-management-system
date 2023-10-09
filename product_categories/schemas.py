from pydantic import (
    BaseModel,
    field_validator,
)

from validators import validate_string


class CategoryBase(BaseModel):
    name: str


class CreateCategory(BaseModel):
    name: str

    @field_validator("name")
    def validate_name(cls, name):
        return validate_string(
            name,
            r"^[A-Za-z][A-Za-z0-9\s]*$",
            "Name must only contain letters, "
            "numbers, spaces and start with letter"
        )


class UpdateCategory(CreateCategory):
    name: str = None


class Category(CategoryBase):
    id: int

    class Config:
        orm_mode: True


class DeleteCategory(BaseModel):
    message: str
