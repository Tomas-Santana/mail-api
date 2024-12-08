from pydantic import BaseModel, field_validator

class RegisterRequest(BaseModel):
  username: str
  password: str
  full_name: str
  
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
  @field_validator("full_name")
  def full_name_must_not_be_empty(cls, full_name: str):
    if not full_name:
      raise ValueError("full_name must not be empty")
    return full_name