from fastapi import FastAPI
import models
from database import engine
from routers import blog, user, authentication


app = FastAPI(
    title="FastAPI Tutorial",
    description="This is a simple tutorial for FastAPI",
    version="1.0.0",
)

# Include routers
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)

# Create all database tables
# This line creates all tables defined in models.py if they don't exist
# Base.metadata.create_all() scans all SQLAlchemy models and creates corresponding tables
models.Base.metadata.create_all(engine)


# The /blog endpoint now uses dependency injection to get a DB session
# @app.post(
#     "/blog",
#     status_code=status.HTTP_201_CREATED,
#     response_model=schemas.ShowBlog,
#     tags=["blogs"],
# )
# def create(request: schemas.Blog, db: Session = Depends(get_db)):
#     # For demo, assign user_id=1 or get from request/session
#     new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
#     db.add(new_blog)  # Add the new blog to the session
#     db.commit()  # Commit the transaction to save it in the database
#     db.refresh(new_blog)  # Refresh to get any DB-generated fields (like ID)
#     return new_blog  # Return the newly


# Get all blogs
# @app.get(
#     "/blog",
#     status_code=status.HTTP_200_OK,
#     response_model=List[schemas.ShowBlog],
#     tags=["blogs"],
# )
# def all(db: Session = Depends(get_db)):
#     blogs = db.query(models.Blog).all()
#     return blogs


# # Get the blog with Id
# @app.get("/blog/{id}", status_code=200, response_model=schemas.ShowBlog, tags=["blogs"])
# def blog(id: int, db: Session = Depends(get_db)):
#     blog = db.query(models.Blog).filter(models.Blog.id == id).first()
#     if not blog:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Blog with id {id} is not available",
#         )
#     return blog


# # Delete the blog
# @app.delete("/blog/{id}", status_code=status.HTTP_200_OK, tags=["blogs"])
# def destroy(id: int, db: Session = Depends(get_db)):
#     blog = db.query(models.Blog).filter(models.Blog.id == id)
#     if not blog.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

#     blog.delete(synchronize_session=False)
#     db.commit()
#     return {"detail": "Deleted Successfully"}


# # Update the blog with Id
# @app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["blogs"])
# def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
#     blog_query = db.query(models.Blog).filter(models.Blog.id == id)
#     if not blog_query.first():
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Blog not found",
#         )
#     blog_query.update(
#         {models.Blog.title: request.title, models.Blog.body: request.body},
#         synchronize_session=False,
#     )
#     db.commit()
#     return {"details": "Successfully updated the blog"}


# # Create User
# @app.post(
#     "/user",
#     response_model=schemas.ShowUser,
#     status_code=status.HTTP_201_CREATED,
#     tags=["users"],
# )
# def createUser(request: schemas.User, db: Session = Depends(get_db)):
#     existing_user = (
#         db.query(models.User).filter(models.User.email == request.email).first()
#     )
#     if existing_user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="User with this email already exists",
#         )
#     hashedPassword = Hash.bcrypt(request.password)
#     user = models.User(name=request.name, password=hashedPassword, email=request.email)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="User is not created"
#         )
#     dbOps(user, db)
#     return user


# # get user
# @app.get("/user/{email}", response_model=schemas.ShowUser, tags=["users"])
# def getUser(email: str, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.email == email).first()
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="User is not present"
#         )
#     return user  # SQLAlchemy will load blogs due to relationship
