import re

from .db import Base, db
from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy import String, Boolean, Text
from asyncio import run


class User(Base):
    __tablename__ = "user"
    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    surname: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(Text(), nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(String(11), nullable=False, unique=True)

    @validates("email")
    def email_validates(self, key, email):
        if re.match(r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", email) is None:
            raise ValueError("Ошибка валидации почты")
        return email

    @validates("phone_number")
    def phone_number_validates(self, key, phone_number):
        if re.match(r"^7\d{10}$", phone_number) is None:
            return ValueError("Ошибка валидации номера телефона")
        return phone_number

    def __repr__(self):
        return f"User({self.user_id}, {self.email}, {self.first_name} {self.surname}, {self.last_name})"


async def init_models():
    async with db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    run(init_models())