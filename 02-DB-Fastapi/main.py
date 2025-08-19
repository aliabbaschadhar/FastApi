from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
import models
import schemas
from database import (
    engine,
    SessionLocal,
)  # SessionLocal is imported to create DB sessions
from sqlalchemy.orm import Session
from hashing import Hash


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


def dbOps(param, db: Session = Depends(get_db)):
    db.add(param)
    db.commit()
    db.refresh(param)


# The /blog endpoint now uses dependency injection to get a DB session
@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    # Create a new Blog object from the request data
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)  # Add the new blog to the session
    db.commit()  # Commit the transaction to save it in the database
    db.refresh(new_blog)  # Refresh to get any DB-generated fields (like ID)
    return new_blog  # Return the newly


# Get all blogs
@app.get("/blog", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


# Get the blog with Id
@app.get("/blog/{id}", status_code=200, response_model=schemas.ShowBlog)
def blog(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} is not available",
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"details": f"Blog with id  {id} is not available"}
    return blog


# Delete the blog
@app.delete("/blog/{id}", status_code=status.HTTP_200_OK)
def destroy(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    blog.delete(synchronize_session=False)

    db.commit()
    return {"detail": "Deleted Successfully"}


# Update the blog with Id
@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog_query = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found",
        )
    blog_query.update(
        {models.Blog.title: request.title, models.Blog.body: request.body},
        synchronize_session=False,
    )
    db.commit()
    return {"details": "Successfully updated the blog"}


# Create User
@app.post("/user")
def createUser(request: schemas.User, db: Session = Depends(get_db)):
    hashedPassword = Hash.bcrypt(request.password)
    user = models.User(name=request.name, password=hashedPassword, email=request.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User is not created"
        )
    dbOps(user, db)
    return user
