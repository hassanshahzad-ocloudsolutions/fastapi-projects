
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional


#Because of pydantic automatic data validation will be handled
# Field(...) means this field is required
class Book(BaseModel):
    id: UUID 
    title: str = Field(...,min_length=2, max_length=50)
    author: str = Field(...,min_length=3, max_length=20)
    description: Optional[str] = Field(None,title="Description of Book", min_length=1, max_length=100)
    rating: int = Field(..., ge=0, le=100)

'''this class is made so we can return the book without rating attribute
it is similar to use case when user login using id and password and when we send response back to the user we only send id'''
class BookNoRating(BaseModel):
    id: UUID 
    title: str = Field(...,min_length=2, max_length=50)
    author: str = Field(...,min_length=3, max_length=20)
    description: Optional[str] = Field(None,title="Description of Book", min_length=1, max_length=100)
