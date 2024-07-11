from .db import db
from .model import User
from sqlalchemy import select
from werkzeug.security import generate_password_hash


async def create_user(data: dict) -> None:
    async with db.async_session() as session:
        data["password"] = generate_password_hash(data["password"])
        print(data["password"])
        user = User(**data)
        session.add(user)
        await session.flush()
        await session.commit()


async def get_user_for_email(email: str) -> User | None:
    async with db.async_session() as session:
        query = select(User).where(User.email == email)
        result = await session.execute(query)
        return result.scalar()


async def get_user_for_id(user_id: str):
    async with db.async_session() as session:
        result = await session.get(User, int(user_id))
        return result
