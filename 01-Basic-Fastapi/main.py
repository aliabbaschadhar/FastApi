from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
# import uvicorn


app = FastAPI()


@app.get("/")
def index():
    return {"data": "blog_list"}


# It's important to define static routes before dynamic routes in FastAPI.
# If you put the dynamic route (with a path parameter) first, it may "catch" requests meant for the static route.
# For example, if "/blog/{blog_id}" is defined before "/blog/unpublished", a request to "/blog/unpublished"
# will treat "unpublished" as a blog_id, which is not intended.

# @app.get("/blog/{blog_id}")
# def show(blog_id: int):
#     # This is a dynamic route that matches any integer blog_id.
#     return {"id": blog_id}


@app.get("/blog/unpublished")
def unpublished():
    # This is a static route, so it should be defined before the dynamic route below.
    return {"data": "all unpublished blogs"}


@app.get("/blog/{blog_id}")
def show(blog_id: int):
    # This is a dynamic route that matches any integer blog_id.
    return {"id": blog_id}


@app.get("/blog/{blog_id}/comments")
def comments(blog_id):
    return {"data": {blog_id: {"comments": {"1", "2", "3"}}}}


@app.get("/blogs")
def blogs(limit: int = 10, published: bool = True, sort: Optional[str] = None):
    # limit, published, sort are query parameters
    # first 2 are mandatory and 3rd one is optional of type string
    if published and sort:
        return {"data": f"{limit} published blogs from the DB {sort}"}
    else:
        return {"data": f"{limit} blogs from the DB"}


# Pydantic is a Python library that provides data validation and parsing based on Python type annotations.
# It ensures that the data you receive matches the expected types and structure, raising errors if not.
# In FastAPI, Pydantic models are used to define the shape and types of data for request bodies, query parameters, and responses.
# A Pydantic model is a Python class that inherits from BaseModel and uses type hints to specify the expected fields.
# FastAPI automatically uses these models to validate incoming data and generate API documentation.
# BaseModel is the foundational class in Pydantic; it provides features like automatic type validation, serialization, and helpful error messages.


class Blog(BaseModel):
    title: str  # The title of the blog post. Must be a string.
    body: str  # The main content of the blog post. Must be a string.
    published: Optional[bool] = (
        False  # Indicates if the blog is published. Optional; defaults to False.
    )
    created_at: datetime = (
        datetime.now()
    )  # The date and time the blog was created. Defaults to the current time.


@app.post("/blog")
def create_blog(request: Blog):
    return {
        "data": {
            "title": request.title,
            "body": request.body,
            "created_at": request.created_at,
            "published": request.published,
            "message": (
                "Blog is published."
                if request.published
                else "Blog is not published yet!"
            ),
        }
    }


# If you want to change the port number then
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=3000)
