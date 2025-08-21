from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
import models
import schemas
import database
from sqlalchemy.orm import Session


router = APIRouter(prefix="/blog", tags=["blogs"])


# Get all blogs
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


# Get the blog with Id
@router.get(
    "/{id}",
    status_code=200,
    response_model=schemas.ShowBlog,
)
def blog(id: int, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} is not available",
        )
    return blog


# Create a blog


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ShowBlog,
)
def create(request: schemas.Blog, db: Session = Depends(database.get_db)):
    # For demo, assign user_id=1 or get from request/session
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    database.dbOps(new_blog, db)
    return new_blog


# Delete the blog
@router.delete(
    "/{id}",
    status_code=status.HTTP_200_OK,
)
def destroy(id: int, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    blog.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Deleted Successfully"}


# Update the blog with Id
@router.put(
    "/{id}",
    status_code=status.HTTP_202_ACCEPTED,
)
def update(id: int, request: schemas.Blog, db: Session = Depends(database.get_db)):
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
