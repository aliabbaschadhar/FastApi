from fastapi import FastAPI
import models
import schemas
from database import engine

app = FastAPI()

# Create all database tables
# This line creates all tables defined in models.py if they don't exist
# Base.metadata.create_all() scans all SQLAlchemy models and creates corresponding tables
models.Base.metadata.create_all(engine)


@app.post("/blog")
def create(request: schemas.Blog):
    return request
