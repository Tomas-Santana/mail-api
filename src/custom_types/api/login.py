from pydantic import BaseModel
from pydantic import BaseModel, field_validator

class LoginRequest(BaseModel):
  username: str
  password: str
  
  @field_validator("username")
  def username_must_not_be_empty(cls, username: str):
    if not username:
      raise ValueError("username must not be empty")
    return username
  @field_validator("password")
  def password_min_length(cls, password: str):
    if len(password) < 8:
      raise ValueError("password must be at least 8 characters long")
    return password
