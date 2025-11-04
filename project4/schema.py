#pydantics data validation file

from pydantic import BaseModel, Field
from typing import Optional

class TodoAdd(BaseModel):
    title : str = Field(...,max_length=20)
    description: str = Field(..., max_length=50)
    priority: int = Field(...,ge=1, le=10, description="The priority must be between 1 to 10")
    complete: bool = Field(...)

class TodoUpdate(BaseModel):
    description: str = Field(..., max_length=50)
    complete: bool = Field(...)

class CreateUser(BaseModel):
    username: str
    email: Optional[str] = None
    first_name: str
    last_name: str
    password: str

class UserDetails(BaseModel):
    username: str
    email: Optional[str] = None
    first_name: str
    last_name: str

class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str




