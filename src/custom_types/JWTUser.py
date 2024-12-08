from pydantic import BaseModel

class JWTUser(BaseModel):
    username: str
    full_name: str
    id: str
    mail_password: str
    