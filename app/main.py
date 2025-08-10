from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
import time
import logging
from contextlib import asynccontextmanager

from app.api.api import api_router
from app.core.config import settings
from app.db.base import Base, engine
from app.db.optimize import optimize_database

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database tables and optimize
    logger.info("Initializing database...")
    Base.metadata.create_all(bind=engine)
    optimize_database()
    logger.info("Database initialized successfully.")
    
    yield
    
    # Shutdown: Clean up resources
    logger.info("Shutting down...")

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add middleware for request timing
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"Request to {request.url.path} processed in {process_time:.4f} seconds")
    return response

# Mount static files
os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)
app.mount("/static", StaticFiles(directory=settings.UPLOAD_FOLDER), name="static")

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {"message": "Welcome to Snapped AI API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Exception handler for unexpected errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        host=settings.HOST, 
        port=settings.PORT,
        reload=True
    )