from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str = Field(min_length=1)
    household_name: str = Field(default="Mon foyer", min_length=1)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"