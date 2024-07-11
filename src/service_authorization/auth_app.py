import json
from datetime import timedelta

from jwt.exceptions import InvalidTokenError
from settings.config import settings, redis_client
from schemas import RegisterUserSchema, AuthUserSchema, JWTSchema, UserSchema, AuthResponseSchema
from fastapi import APIRouter, HTTPException, Depends, FastAPI, Cookie, Response
from fastapi.security import HTTPBearer
from func_service import encode_jwt, decode_jwt, get_cookie_data, post_data_for_api, generate_cookie_session_id, delete_cookie, set_auth_cookie
from fastapi.responses import RedirectResponse, JSONResponse
from database.requests_model import get_user_for_email, create_user, get_user_for_id
from werkzeug.security import check_password_hash

router = APIRouter(
    prefix="/auth",
    tags=['Auth']
)

http_bearer = HTTPBearer()

app = FastAPI()


@router.post("/login")
async def login_user_jwt(user: AuthUserSchema, response: Response):
    user_info = await get_user_for_email(user.email)
    if user_info is not None and check_password_hash(user_info.password, user.password):
        payload_jwt = {
            "sub": user_info.user_id,
            "email": user_info.email
        }
        cooke_session_id: str = generate_cookie_session_id()
        token = encode_jwt(payload=payload_jwt)
        set_auth_cookie(cooke_session_id, token, response)
        return AuthResponseSchema(
            access_token=token,
            token_type="Bearer",
            cooke_session_id=cooke_session_id
        )
    raise HTTPException(status_code=403, detail="Password or email is bad")


@router.get("/get_me")
async def get_user_for_token(payload: dict = Depends(get_cookie_data)):
    user_id: str | None = payload.get("sub")
    if user_id is not None:
        user = await get_user_for_id(user_id)
        print(user_id)
        return UserSchema(
            first_name=user.first_name,
            surname=user.surname,
            last_name=user.last_name,
            email=user.email,
            phone_number=user.phone_number
        )
    raise HTTPException(status_code=406, detail="User is not found for token")


@router.get("/check_auth_token")
def check_auth(payload: dict = Depends(get_cookie_data)):
    try:
        return payload
    except InvalidTokenError as e:
        return RedirectResponse("/login")


@router.post("/register")
async def register_user(user: RegisterUserSchema, response: Response):
    try:
        usr = await get_user_for_email(user.email)
        if usr:
            raise HTTPException(status_code=403, detail="Такой пользователь уже существует")
        await create_user(user.model_dump())
        request_login = await post_data_for_api(url=settings.url_api.login_user,
                                            data={"email": user.email, "password": user.password})
        token = request_login["access_token"]
        cooke_session_id = request_login["cooke_session_id"]
        set_auth_cookie(cooke_session_id, token, response)
        return request_login
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e)


@router.get("/logout")
def logout_user(payload: dict = Depends(delete_cookie)):
    return Response(status_code=307)


app.include_router(router)