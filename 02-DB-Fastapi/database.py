# Database Configuration and Setup
# This file configures the SQLAlchemy database connection and session management

# Import SQLAlchemy components
from sqlalchemy import create_engine  # Creates database engine
from sqlalchemy.ext.declarative import declarative_base  # Base class for ORM models
from sqlalchemy.orm import sessionmaker  # Creates database sessions

# Database URL configuration
# SQLite database connection string pointing to a local file named 'blog.db'
# Format: sqlite:///./filename.db (relative path to current directory)
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

# Create database engine
# The engine is the starting point for any SQLAlchemy application
# connect_args={"check_same_thread": False} is required for SQLite to work with FastAPI
# This disables SQLite's thread safety check since FastAPI uses multiple threads
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create SessionLocal class
# This class will be used to create database sessions
# autocommit=False: We'll manually commit transactions
# autoflush=False: We'll manually flush changes to the database
# bind=engine: This session factory is bound to our database engine
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Create Base class
# This will be the base class for all our ORM models
# All database models will inherit from this Base class
Base = declarative_base()
