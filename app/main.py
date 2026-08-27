from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.database.database import Base, engine, SessionLocal
from app.database.seed import seed_demo_data
from app.auth.router import router as auth_router
from app.task.router import router as task_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_demo_data(db)
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Interview-oriented Task Management REST API",
    lifespan=lifespan,
)

register_exception_handlers(app)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(task_router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy", "service": settings.app_name}
