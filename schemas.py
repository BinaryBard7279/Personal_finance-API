from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date


class TransactionCreate(BaseModel):
    amount: int = Field(gt=0)
    category: str = Field(min_length=1)
    description: Optional[str] = None
    date: date  
    type: str


class Transaction(BaseModel):
    id: int
    amount: int
    category: str
    description: Optional[str]
    date: date  
    type: str
    owner_id: int
    
    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6)


class User(BaseModel):
    id: int
    username: str
    email: str
    is_admin: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str