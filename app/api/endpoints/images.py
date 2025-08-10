from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import os

from app.db.base import get_db
from app.models.schemas import ImageUploadResponse, ImageClipResponse, SimilarProductsResponse, SearchResult
from app.utils.image_processing import save_upload_file, clip_image, is_allowed_file
from app.services.serpapi_service import search_similar_products
from app.services.db_service import create_image_search, create_search_results, get_search_by_id, get_recent_searches
from app.core.config import settings

router = APIRouter()

@router.post("/upload", response_model=ImageUploadResponse)
async def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload an image for product search
    """
    # Check if file is allowed
    if not is_allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="File type not allowed")
    
    # Save the uploaded file
    file_path = await save_upload_file(file)
    
    return {"image_path": file_path, "message": "Image uploaded successfully"}

@router.post("/clip", response_model=ImageClipResponse)
async def clip_uploaded_image(
    image_path: str = Form(...),
    x: int = Form(...),
    y: int = Form(...),
    width: int = Form(...),
    height: int = Form(...)
):
    """
    Clip an uploaded image to the specified dimensions
    """
    # Check if the file exists
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    try:
        # Clip the image
        clipped_image_path = await clip_image(image_path, x, y, width, height)
        return {"image_path": clipped_image_path, "message": "Image clipped successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clipping image: {str(e)}")

@router.post("/search", response_model=SimilarProductsResponse)
async def search_products(
    image_path: str = Form(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db)
):
    """
    Search for similar products using the uploaded image
    
    This endpoint is optimized for fast response times by:
    1. Using background tasks for database operations
    2. Caching search results
    3. Implementing retries with exponential backoff
    4. Running CPU-intensive operations in a thread pool
    """
    # Check if the file exists
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    try:
        # Create a new search record
        db_search = await create_image_search(db, image_path)
        
        # Convert local file path to URL for SerpAPI
        # In a production environment, you would upload the image to a public URL
        # For this example, we'll assume the image is accessible via a URL
        image_url = f"https://work-1-tvbntogukqxzeggf.prod-runtime.all-hands.dev/static/{os.path.basename(image_path)}"
        
        # Search for similar products (this is cached and optimized)
        similar_products = await search_similar_products(image_url)
        
        # Store search results in the database as a background task
        # This allows us to return the response to the user faster
        # while the database operations continue in the background
        background_tasks.add_task(
            create_search_results, db, db_search.id, similar_products
        )
        
        # Convert results to schema models
        # We don't need to wait for the database operation to complete
        results = [
            SearchResult(
                id=0,  # Temporary ID since we're not waiting for DB
                search_id=db_search.id,
                title=product.get("title"),
                link=product.get("link"),
                source=product.get("source"),
                price=product.get("price"),
                thumbnail=product.get("thumbnail"),
                description=product.get("snippet"),
                rating=product.get("rating"),
                reviews_count=product.get("reviews")
            )
            for product in similar_products
        ]
        
        return {
            "search_id": db_search.id,
            "search_time": db_search.search_time,
            "image_path": db_search.image_path,
            "results": results,
            "total_results": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching for products: {str(e)}")

@router.get("/searches/{search_id}", response_model=SimilarProductsResponse)
async def get_search_results(
    search_id: int,
    db: Session = Depends(get_db)
):
    """
    Get the results of a previous search
    """
    # Get the search record
    db_search = await get_search_by_id(db, search_id)
    
    if not db_search:
        raise HTTPException(status_code=404, detail="Search not found")
    
    # Convert DB results to schema models
    results = [
        SearchResult(
            id=result.id,
            search_id=result.search_id,
            title=result.title,
            link=result.link,
            source=result.source,
            price=result.price,
            thumbnail=result.thumbnail,
            description=result.description,
            rating=result.rating,
            reviews_count=result.reviews_count
        )
        for result in db_search.results
    ]
    
    return {
        "search_id": db_search.id,
        "search_time": db_search.search_time,
        "image_path": db_search.image_path,
        "results": results,
        "total_results": len(results)
    }

@router.get("/searches", response_model=List[SimilarProductsResponse])
async def get_recent_search_results(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get recent search results
    """
    # Get recent searches
    db_searches = await get_recent_searches(db, skip, limit)
    
    # Convert DB searches to schema models
    searches = []
    for db_search in db_searches:
        results = [
            SearchResult(
                id=result.id,
                search_id=result.search_id,
                title=result.title,
                link=result.link,
                source=result.source,
                price=result.price,
                thumbnail=result.thumbnail,
                description=result.description,
                rating=result.rating,
                reviews_count=result.reviews_count
            )
            for result in db_search.results
        ]
        
        searches.append({
            "search_id": db_search.id,
            "search_time": db_search.search_time,
            "image_path": db_search.image_path,
            "results": results,
            "total_results": len(results)
        })
    
    return searches