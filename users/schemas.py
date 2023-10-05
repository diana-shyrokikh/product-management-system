from pydantic import (
    BaseModel,
    field_validator,
)

from validators import (
    validate_string,
    validate_phone_number_format
)


class UserBase(BaseModel):
    username: str
    email: str
    phone_number: str


class CreateUser(BaseModel):
    username: str
    email: str
    phone_number: str
    password: str

    @field_validator("username")
    def validate_username(cls, username):
        return validate_string(
            username,
            r"^[a-z][a-z0-9]*$",
            "Username must only contain letters, numbers "
            "and begin with letter"
        )

    @field_validator("email")
    def validate_email(cls, email):
        return validate_string(
            email,
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "Invalid email address"
        )

    @field_validator("password")
    def validate_password(cls, password):
        return validate_string(
            password,
            r"^[A-Za-z][A-Za-z0-9!$%&*_+\-./\\,]*$",
            "Password can contain letters, "
            "numbers and symbols: "
            r"!, $, %, &, *, _, +, \, /, -, ."
        )

    @field_validator("phone_number")
    def validate_phone_number(cls, phone_number):
        return validate_phone_number_format(phone_number)


class UpdateUser(CreateUser):
    username: str = None
    email: str = None
    phone_number: str = None
    password: str = None


class User(UserBase):
    id: int

    class Config:
        orm_mode: True


class DeleteUser(BaseModel):
    message: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
