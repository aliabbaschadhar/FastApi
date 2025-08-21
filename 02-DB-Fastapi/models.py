# Database Models (SQLAlchemy ORM Models)
# This file defines the database table structure using SQLAlchemy ORM

# Import SQLAlchemy column types and the Base class
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
)  # Column types for defining table structure
from database import Base  # Base class from our database configuration
from sqlalchemy.orm import relationship


class Blog(Base):
    # Define the table name in the database
    __tablename__ = "blogs"

    # Define table columns
    # id: Primary key column (auto-incrementing integer with index for faster queries)
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="blogs")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    name = Column(String)
    password = Column(String)
    blogs = relationship("Blog", back_populates="user")
