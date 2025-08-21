from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
import models
import schemas
import database
import oauth2
from sqlalchemy.orm import Session


router = APIRouter(prefix="/blog", tags=["Blogs"])


# Get all blogs (public route)
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
def get_all_blogs(db: Session = Depends(database.get_db)):
    """
    Get all blogs from all users. Public endpoint.

    Args:
        db: Database session

    Returns:
        List of all blogs with user information
    """
    blogs = db.query(models.Blog).all()
    return blogs


# Get blogs by current user (protected route)
@router.get(
    "/my-blogs", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog]
)
def get_my_blogs(
    current_user: models.User = Depends(oauth2.get_current_user),
    db: Session = Depends(database.get_db),
):
    """
    Get all blogs created by the current authenticated user.

    Args:
        current_user: Current authenticated user
        db: Database session

    Returns:
        List of blogs created by the current user
    """
    blogs = db.query(models.Blog).filter(models.Blog.user_id == current_user.id).all()
    return blogs


# Get blog by ID (public route)
@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShowBlog,
)
def get_blog_by_id(id: int, db: Session = Depends(database.get_db)):
    """
    Get a specific blog by ID. Public endpoint.

    Args:
        id: Blog ID
        db: Database session

    Returns:
        Blog with user information

    Raises:
        HTTPException: If blog not found
    """
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} not found",
        )
    return blog


# Create a blog (protected route)
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ShowBlog,
)
def create_blog(
    request: schemas.Blog,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    """
    Create a new blog post. Requires authentication.

    Args:
        request: Blog data (title, body)
        db: Database session
        current_user: Current authenticated user

    Returns:
        Created blog with user information
    """
    new_blog = models.Blog(
        title=request.title, body=request.body, user_id=current_user.id
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# Delete blog (protected route - only owner can delete)
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_blog(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    """
    Delete a blog post. Only the blog owner can delete their blog.

    Args:
        id: Blog ID to delete
        db: Database session
        current_user: Current authenticated user

    Returns:
        Success message

    Raises:
        HTTPException: If blog not found or user not authorized
    """
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
        )

    # Check if current user is the owner of the blog
    if getattr(blog, "user_id") != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this blog",
        )

    db.delete(blog)
    db.commit()
    return {"detail": "Blog deleted successfully"}


# Update blog (protected route - only owner can update)
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(
    id: int,
    request: schemas.Blog,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    """
    Update a blog post. Only the blog owner can update their blog.

    Args:
        id: Blog ID to update
        request: Updated blog data (title, body)
        db: Database session
        current_user: Current authenticated user

    Returns:
        Success message

    Raises:
        HTTPException: If blog not found or user not authorized
    """
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found",
        )

    # Check if current user is the owner of the blog
    if getattr(blog, "user_id") != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this blog",
        )

    # Update blog fields using SQLAlchemy update method
    db.query(models.Blog).filter(models.Blog.id == id).update(
        {models.Blog.title: request.title, models.Blog.body: request.body}
    )
    db.commit()

    return {"detail": "Blog updated successfully"}
