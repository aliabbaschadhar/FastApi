from fastapi import FastAPI, Depends
import models
import schemas
from database import (
    engine,
    SessionLocal,
)  # SessionLocal is imported to create DB sessions
from sqlalchemy.orm import Session

app = FastAPI()

# Create all database tables
# This line creates all tables defined in models.py if they don't exist
# Base.metadata.create_all() scans all SQLAlchemy models and creates corresponding tables
models.Base.metadata.create_all(engine)


# Dependency function to provide a database session for each request
def get_db():
    db = SessionLocal()  # Create a new database session
    try:
        yield db  # Yield the session to be used in the request
    finally:
        db.close()  # Ensure the session is closed after the request


# The /blog endpoint now uses dependency injection to get a DB session
@app.post("/blog")
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    # Create a new Blog object from the request data
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)  # Add the new blog to the session
    db.commit()  # Commit the transaction to save it in the database
    db.refresh(new_blog)  # Refresh to get any DB-generated fields (like ID)
    return new_blog  # Return the newly


@app.get("/blog")
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{id}")
def blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    return blog
