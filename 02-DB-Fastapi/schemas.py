# Pydantic Schemas for Data Validation
# This file defines the data models used for API request/response validation and serialization

# Import Pydantic BaseModel for creating data validation schemas
from pydantic import BaseModel
from typing import List, Optional


class Blog(BaseModel):
    """
    Blog schema for API request/response validation.

    This Pydantic model defines the structure and validation rules for blog data
    that will be sent to and received from the API endpoints.

    Attributes:
        title (str): The title of the blog post (required string)
        body (str): The content/body of the blog post (required string)

    Note:
    - This schema is used for validating incoming JSON data in API requests
    - It automatically converts JSON to Python objects and validates data types
    - FastAPI uses this schema to generate OpenAPI documentation
    - Unlike the SQLAlchemy model, this doesn't include 'id' since it's auto-generated
    """

    # Blog post title - required string field
    title: str

    # Blog post content - required string field
    body: str


# Response Models ==> Let's say in response we don't want to show the Id of the blog then we can create a  response model


class User(BaseModel):
    email: str
    password: str
    name: str


# Minimal user schema for blog responses (no blogs to avoid recursion)
class UserInBlog(BaseModel):
    id: int
    email: str
    name: str

    class Config:
        from_attributes = True


# Minimal blog schema for user responses (no user to avoid recursion)
class BlogInUser(BaseModel):
    id: int
    title: str
    body: str

    class Config:
        from_attributes = True


class ShowBlog(Blog):
    id: int
    user: Optional[UserInBlog]  # Use minimal user schema

    class Config:
        from_attributes = True


class ShowUser(BaseModel):
    id: int
    email: str
    name: str
    blogs: List[BlogInUser] = []

    class Config:
        from_attributes = True


class Login(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True
