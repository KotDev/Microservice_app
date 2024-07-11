import uuid
from datetime import timedelta, datetime

import aiohttp
import jwt
from jwt.exceptions import InvalidTokenError
from settings.config import settings, redis_client
from fastapi import Cookie, HTTPException, Response


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded


def generate_cookie_session_id() -> str:
    return uuid.uuid4().hex


def set_auth_cookie(cooke_session_id: str, token: str | bytes, response: Response) -> None:
    redis_client.setex(cooke_session_id,
                       time=timedelta(minutes=settings.auth_jwt.access_token_expire_minutes),
                       value=token)
    response.set_cookie(settings.cookie_auth.cookie_key, cooke_session_id)


def get_cookie_data(cookie_session_id: str | None = Cookie(alias=settings.cookie_auth.cookie_key)) -> dict:
    data: bytes = redis_client.get(cookie_session_id)
    print(data)
    print("\n")
    print(cookie_session_id)
    if data is None:
        raise HTTPException(status_code=403, detail="User is not autntificated")
    try:
        payload = decode_jwt(data)
        return dict(payload)
    except InvalidTokenError as e:
        raise HTTPException(status_code=406, detail="User is not found for token")


def delete_cookie(cookie_session_id: str | None = Cookie(alias=settings.cookie_auth.cookie_key)):
    redis_client.delete(cookie_session_id)


async def get_data_for_api(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return {"error": "Error api request get"}


async def post_data_for_api(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                return await response.json()
            else:
                return {"error": "Error api request post"}

