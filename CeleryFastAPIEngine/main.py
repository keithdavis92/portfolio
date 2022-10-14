from fastapi import FastAPI

from routes.routes import api_router
from utils.celery_utils import create_celery
from utils.file_utils import clean_temp_files


def create_app() -> FastAPI:
    current_app = FastAPI(
        title="Asynchronous CSV file aggregation", description="", version="1.0.0",
    )

    current_app.celery_app = create_celery()
    current_app.include_router(api_router)
    return current_app


app = create_app()
celery = app.celery_app


@app.on_event("startup")
async def startup():
    # Ensure temp files dir is empty to minimise bloat
    clean_temp_files()


@app.on_event("shutdown")
async def shutdown():
    # Ensure temp files dir is empty to minimise bloat
    clean_temp_files()
