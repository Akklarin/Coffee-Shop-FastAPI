import uvicorn
from fastapi import FastAPI

from .api import main_router
from src.core.config import settings


app = FastAPI(
    title=settings.PROJECT_TITLE,
    description=settings.PROJECT_DESCRIPTION,
    docs_url=settings.PROJECT_DOCS_URL
    )

app.include_router(main_router)


@app.on_event("startup")
async def on_startup():
    from src.core.database import create_tables
    await create_tables()

# python -m src.main

if __name__ == '__main__':
    uvicorn.run(
        'src.main:app',
        host=settings.PROJECT_HOST,
        port=settings.PROJECT_PORT,
    )
