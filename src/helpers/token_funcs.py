from custom_types.JWTUser import JWTUser
from jwt import decode, InvalidTokenError, encode
from dotenv import load_dotenv
import os
from custom_types.models.User import User
load_dotenv(override=True)
SECRET = os.getenv("JWT_SECRET")

def get_user_from_token(token: str) -> JWTUser | None:
    try:
        return JWTUser(**decode(token, SECRET, algorithms=["HS256"]))
    except InvalidTokenError:
        return None
    
def get_token_from_user(user: User) -> str:
    jwt_user = JWTUser(username=user.username, full_name=user.full_name, mail_password=user.mail_password, id=str(user._id))
    return encode(jwt_user.model_dump(), SECRET, algorithm="HS256")