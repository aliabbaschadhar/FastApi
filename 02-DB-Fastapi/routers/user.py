from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
import schemas
import database
import oauth2

router = APIRouter(prefix="/user", tags=["Users"])


# Get current user profile
@router.get("/me", response_model=schemas.ShowUser)
def get_current_user_profile(
    current_user: models.User = Depends(oauth2.get_current_user),
):
    """
    Get the current authenticated user's profile information.

    Args:
        current_user: Current authenticated user from JWT token

    Returns:
        User profile with blogs
    """
    return current_user


# Get user by ID (protected route)
@router.get("/{user_id}", response_model=schemas.ShowUser)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    """
    Get user profile by ID. Requires authentication.

    Args:
        user_id: ID of the user to retrieve
        db: Database session
        current_user: Current authenticated user

    Returns:
        User profile with blogs

    Raises:
        HTTPException: If user not found
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


# Get user by email (protected route)
@router.get("/email/{email}", response_model=schemas.ShowUser)
def get_user_by_email(
    email: str,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    """
    Get user profile by email. Requires authentication.

    Args:
        email: Email of the user to retrieve
        db: Database session
        current_user: Current authenticated user

    Returns:
        User profile with blogs

    Raises:
        HTTPException: If user not found
    """
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user
