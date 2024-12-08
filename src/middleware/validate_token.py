from helpers.token_funcs import get_user_from_token
from flask import Request
from custom_types.JWTUser import JWTUser

def validate_token(request: Request) -> JWTUser | None:
    header = request.headers.get("Authorization")
    if not header:
        return None
    token = header.split(" ")[1]
    user = get_user_from_token(token)
    return user
