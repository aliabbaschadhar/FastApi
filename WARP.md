# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Structure

This repository contains two FastAPI tutorial projects demonstrating progressive complexity:

### 01-Basic-Fastapi
Basic FastAPI application with simple endpoints, query parameters, and Pydantic models. Entry point: `main.py`

### 02-DB-Fastapi  
Full-featured FastAPI application with SQLAlchemy database, JWT authentication, and modular router architecture.

## Common Development Commands

### Running the Applications

**Basic FastAPI (01-Basic-Fastapi):**
```bash
cd 01-Basic-Fastapi
uvicorn main:app --reload --port 8000
```

**Database FastAPI (02-DB-Fastapi):**
```bash
cd 02-DB-Fastapi
uvicorn main:app --reload --port 8000
```

### Package Management
This project uses `uv` for dependency management:
```bash
# Install dependencies
uv sync

# Add new dependency
uv add <package-name>

# Update dependencies
uv lock --upgrade
```

### Development Testing
```bash
# Run basic Python tests (if any test files exist)
python -m pytest

# Test individual endpoints manually
curl -X GET "http://localhost:8000/blog/"
curl -X POST "http://localhost:8000/auth/signup" -H "Content-Type: application/json" -d '{"name":"test","email":"test@example.com","password":"password"}'
```

## Architecture Overview

### 02-DB-Fastapi Architecture

**Core Components:**
- `main.py`: Application entry point with router registration
- `database.py`: SQLAlchemy engine, session management, and database configuration
- `models.py`: SQLAlchemy ORM models (Blog, User tables)
- `schemas.py`: Pydantic models for request/response validation

**Authentication System:**
- `oauth2.py`: JWT token extraction and user authentication
- `jwt_token.py`: JWT token creation and verification
- `hashing.py`: Password hashing using bcrypt
- Authentication flow: signup → login → JWT token → protected endpoints

**Router Structure:**
- `routers/blog.py`: Blog CRUD operations (public + protected routes)
- `routers/user.py`: User management endpoints  
- `routers/authentication.py`: Signup/login endpoints

**Database Design:**
- SQLite database (`blog.db`)
- User-Blog relationship: One user can have many blogs
- Blog ownership enforced in update/delete operations

### Key Patterns

**Dependency Injection:**
- `Depends(database.get_db)`: Database session injection
- `Depends(oauth2.get_current_user)`: Authentication requirement

**Route Protection:**
- Public routes: Get blogs, get single blog
- Protected routes: Create/update/delete blogs, user-specific blogs
- Owner-only operations: Update/delete blogs (users can only modify their own)

**Data Validation:**
- Request models: `schemas.Blog`, `schemas.UserCreate`, `schemas.Login`
- Response models: `schemas.ShowBlog`, `schemas.ShowUser`, `schemas.Token`
- Circular reference prevention in nested models

## Development Notes

**Database Initialization:**
The SQLite database and tables are auto-created on first run via `models.Base.metadata.create_all(engine)`

**Authentication Flow:**
1. User signup → password hashed and stored
2. Login → credentials verified → JWT token returned  
3. Protected endpoints → token validated → user object injected

**Route Ordering:**
Static routes must be defined before dynamic routes (see `01-Basic-Fastapi/main.py` comments)

**API Documentation:**
FastAPI auto-generates OpenAPI docs available at:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)
