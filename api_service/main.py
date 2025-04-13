from fastapi import FastAPI

from core.db import create_db_and_tables
from routers import role, user, project


app = FastAPI(
    title="Project Managment API",
    description="API for Project Management",
    version="1.0.0"
)


app.include_router(project.router)
app.include_router(role.router)
app.include_router(user.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/info", tags=["API"])
def get_info():
    return {
        "name": "Project Management API",
        "version": "1.0.0",
        "description": "API for Project Management"
    }


@app.get("/healthcheck", tags=["API"])
def healthcheck():
    return {
        "status": "ok",
        "message": "API is running"
    }
