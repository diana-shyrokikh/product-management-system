import re

from pydantic import (
    BaseModel,
    field_validator,
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
        pattern = r"^[A-Za-z][A-Za-z0-9]*$"

        if not re.match(pattern, username.strip()):
            raise ValueError(
                "Username must only contain letters, numbers "
                "and begin with letter"
            )

        return username

    @field_validator("email")
    def validate_email(cls, email):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if not re.match(pattern, email.strip()):
            raise ValueError(
                "Email must only contain letters and numbers"
            )

        return email

    @field_validator("password")
    def validate_password(cls, password):
        pattern = r"^[A-Za-z][A-Za-z0-9!$%&*_+\-./\\,]*$"

        if not re.match(pattern, password.strip()):
            raise ValueError(
                "Password can contain letters, "
                "numbers and symbols: "
                r"!, $, %, &, *, _, +, \, /, -, ."
            )

        return password

    @field_validator("phone_number")
    def validate_phone_number(cls, phone_number):
        phone_number = phone_number.replace(" ", "").replace(
            "(", ""
        ).replace(")", "").replace("+", "").replace("-", "")

        if not phone_number.isdigit():
            raise ValueError(
                "Phone number can contain digits, "
                "spaces, symbols: (, +, -, )"
            )

        return phone_number


class UpdateUser(BaseModel):
    username: str = None
    email: str = None
    phone_number: str = None
    password: str = None

    @field_validator("username")
    def validate_username(cls, username):
        if username:
            pattern = r"^[A-Za-z][A-Za-z0-9]*$"

            if not re.match(pattern, username.strip()):
                raise ValueError(
                    "Username must only contain letters, numbers "
                    "and begin with letter"
                )

            return username

    @field_validator("email")
    def validate_email(cls, email):
        if email:
            pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

            if not re.match(pattern, email.strip()):
                raise ValueError(
                    "Email must only contain letters and numbers"
                )

            return email

    @field_validator("password")
    def validate_password(cls, password):
        if password:
            pattern = r"^[A-Za-z][A-Za-z0-9!$%&*_+\-./\\,]*$"

            if not re.match(pattern, password.strip()):
                raise ValueError(
                    "Password can contain letters, "
                    "numbers and symbols: "
                    r"!, $, %, &, *, _, +, \, /, -, ."
                )

            return password

    @field_validator("phone_number")
    def validate_phone_number(cls, phone_number):
        if phone_number:
            phone_number = phone_number.replace(" ", "").replace(
                "(", ""
            ).replace(")", "").replace("+", "").replace("-", "")

            if not phone_number.isdigit():
                raise ValueError(
                    "Phone number can contain digits, "
                    "spaces, symbols: (, +, -, )"
                )

            return phone_number


class User(UserBase):
    id: int

    class Config:
        orm_mode: True


class DeleteUser(BaseModel):
    message: str
