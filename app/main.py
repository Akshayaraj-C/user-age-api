from contextlib import asynccontextmanager
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from app.database import create_db_tables
from app.routers import user
from app.middleware import LoggingMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Automatically create database tables on startup
    await create_db_tables()
    yield

app = FastAPI(title="FastAPI User Age API", lifespan=lifespan)

# Add Request ID and Latency middleware
app.add_middleware(LoggingMiddleware)

# Mount the routes
app.include_router(user.router)

# Scalar documentation route
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API Docs",
    )

@app.get("/health", tags=["healthcheck"])
def health_check():
    return {"status": "healthy"}
