import re
from typing import Annotated
from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, EmailStr, validator


class RegisterUserSchema(BaseModel):
    first_name: Annotated[str, MinLen(3), MaxLen(30)]
    surname: Annotated[str, MinLen(3), MaxLen(30)]
    last_name: Annotated[str, MinLen(3), MaxLen(30)]
    email: EmailStr
    password: str
    phone_number: str

    @validator("email")
    def email_validates(cls, email):
        if re.match(r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", email) is None:
            raise ValueError("Почта введена не корректна")
        return email

    @validator("phone_number")
    def phone_number_validates(cls, phone_number):
        if re.match(r"^7\d{10}$", phone_number) is None:
            raise ValueError("Номера телефона введён не корректно")
        return phone_number

    @validator("password")
    def password_validates(cls, password):
        if re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$', password) is None:
            raise ValueError("Пароль должен содержать хотя бы одну заглавную и строчную букву, "
                             "а так же хотя бы одну цифру и спец символ. Длина паролья не меньше 8 символов")
        return password

    @validator("first_name", "last_name", "surname", allow_reuse=True)
    def fio_validates(cls, data):
        if re.match(r'^([А-Яа-яЁё]{3,})$', data) is None:
            raise ValueError("Не корректные данные для ФИО")
        return data


class AuthUserSchema(BaseModel):
    email: EmailStr
    password: str


class JWTSchema(BaseModel):
    access_token: str
    token_type: str


class AuthResponseSchema(BaseModel):
    access_token: str
    token_type: str
    cooke_session_id: str


class UserSchema(BaseModel):
    first_name: str
    surname: str
    last_name: str
    email: str
    phone_number: str

