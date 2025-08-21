from fastapi import Depends, status, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import database
from hashing import Hash
import models
import schemas
import jwt_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/signup", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
def create_user(request: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """
    Create a new user account.

    Args:
        request: User creation data (name, email, password)
        db: Database session

    Returns:
        Created user information (without password)

    Raises:
        HTTPException: If email already exists
    """
    # Check if user already exists
    existing_user = (
        db.query(models.User).filter(models.User.email == request.email).first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Hash the password
    hashed_password = Hash.bcrypt(request.password)

    # Create new user
    new_user = models.User(
        name=request.name, email=request.email, password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=schemas.Token)
def login_for_access_token(
    request: schemas.Login, db: Session = Depends(database.get_db)
):
    """
    Authenticate user and return JWT access token.

    Args:
        request: Login credentials (email, password)
        db: Database session

    Returns:
        JWT access token and token type

    Raises:
        HTTPException: If credentials are invalid
    """
    # Find user by email
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify password
    if not Hash.verify(request.password, str(user.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=jwt_token.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt_token.create_access_token(
        data={"sub": user.email, "user_id": user.id}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


# Alternative login endpoint using OAuth2PasswordRequestForm (for OpenAPI docs)
@router.post("/token", response_model=schemas.Token)
def login_with_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    """
    OAuth2 compatible token login endpoint.
    Uses username field for email (OAuth2 standard).
    This endpoint is automatically used by FastAPI's interactive docs.
    """
    # Find user by email (username field in OAuth2 form)
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify password
    if not Hash.verify(form_data.password, str(user.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=jwt_token.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt_token.create_access_token(
        data={"sub": user.email, "user_id": user.id}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
