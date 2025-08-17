from fastapi import FastAPI
import models
import schemas
from database import engine

app = FastAPI()

models.Base.metadata.create_all(engine)


@app.post("/blog")
def create(request: schemas.Blog):
    return request
