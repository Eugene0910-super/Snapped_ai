from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from app.models.search import ImageSearch, SearchResult
from app.services.serpapi_service import extract_product_info

async def create_image_search(db: Session, image_path: str) -> ImageSearch:
    """
    Create a new image search record
    
    Args:
        db: Database session
        image_path: Path to the uploaded image
        
    Returns:
        Created ImageSearch object
    """
    db_search = ImageSearch(image_path=image_path)
    db.add(db_search)
    db.commit()
    db.refresh(db_search)
    return db_search

async def create_search_results(db: Session, search_id: int, products: List[Dict[str, Any]]) -> List[SearchResult]:
    """
    Create search result records for a search
    
    Args:
        db: Database session
        search_id: ID of the associated search
        products: List of product dictionaries
        
    Returns:
        List of created SearchResult objects
    """
    db_results = []
    
    for product in products:
        product_info = extract_product_info(product)
        db_result = SearchResult(search_id=search_id, **product_info)
        db.add(db_result)
        db_results.append(db_result)
    
    db.commit()
    
    # Refresh all results to get their IDs
    for result in db_results:
        db.refresh(result)
    
    return db_results

async def get_search_by_id(db: Session, search_id: int) -> Optional[ImageSearch]:
    """
    Get an image search by ID
    
    Args:
        db: Database session
        search_id: ID of the search
        
    Returns:
        ImageSearch object if found, None otherwise
    """
    return db.query(ImageSearch).filter(ImageSearch.id == search_id).first()

async def get_recent_searches(db: Session, skip: int = 0, limit: int = 10) -> List[ImageSearch]:
    """
    Get recent image searches
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of ImageSearch objects
    """
    return db.query(ImageSearch).order_by(ImageSearch.search_time.desc()).offset(skip).limit(limit).all()