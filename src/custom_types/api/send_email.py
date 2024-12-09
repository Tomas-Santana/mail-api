from pydantic import BaseModel, field_validator, EmailStr
from typing import Optional, List

class SendEmailRequest(BaseModel):
    emails: List[EmailStr]
    subject: str
    body: str
    reply_to: Optional[EmailStr] = None
    
    @field_validator("subject")
    def subject_must_not_be_empty(cls, value):
        if not value:
            raise ValueError("Subject must not be empty")
        return value
      
    @field_validator("body")
    def body_must_not_be_empty(cls, value):
        if not value:
            raise ValueError("Body must not be empty")
        return value
    
    