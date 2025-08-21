from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import models
import schemas
import database
import hashing


router = APIRouter(prefix="/user", tags=["users"])


# Create User
@router.post(
    "/",
    response_model=schemas.ShowUser,
    status_code=status.HTTP_201_CREATED,
)
def createUser(request: schemas.User, db: Session = Depends(database.get_db)):
    existing_user = (
        db.query(models.User).filter(models.User.email == request.email).first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    hashedPassword = hashing.Hash.bcrypt(request.password)
    user = models.User(name=request.name, password=hashedPassword, email=request.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User is not created"
        )
    database.dbOps(user, db)
    return user


# get user
@router.get("/{email}", response_model=schemas.ShowUser)
def getUser(email: str, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User is not present"
        )
    return user  # SQLAlchemy will load blogs due to relationship
