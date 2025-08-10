from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional
from datetime import datetime

# Search Result Schema
class SearchResultBase(BaseModel):
    title: Optional[str] = None
    link: Optional[str] = None
    source: Optional[str] = None
    price: Optional[str] = None
    thumbnail: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[float] = None
    reviews_count: Optional[int] = None

class SearchResultCreate(SearchResultBase):
    raw_data: Optional[str] = None

class SearchResult(SearchResultBase):
    id: int
    search_id: int
    
    class Config:
        orm_mode = True

# Image Search Schema
class ImageSearchBase(BaseModel):
    image_path: str

class ImageSearchCreate(ImageSearchBase):
    pass

class ImageSearch(ImageSearchBase):
    id: int
    search_time: datetime
    results: List[SearchResult] = []
    
    class Config:
        orm_mode = True

# Response Schemas
class ImageUploadResponse(BaseModel):
    image_path: str
    message: str = "Image uploaded successfully"

class ImageClipResponse(BaseModel):
    image_path: str
    message: str = "Image clipped successfully"

class SimilarProductsResponse(BaseModel):
    search_id: int
    search_time: datetime
    image_path: str
    results: List[SearchResult]
    total_results: int