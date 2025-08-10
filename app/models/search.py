from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class ImageSearch(Base):
    __tablename__ = "image_searches"

    id = Column(Integer, primary_key=True, index=True)
    image_path = Column(String, nullable=False)
    search_time = Column(DateTime, default=datetime.utcnow)
    
    # Relationship with search results
    results = relationship("SearchResult", back_populates="search", cascade="all, delete-orphan")

class SearchResult(Base):
    __tablename__ = "search_results"

    id = Column(Integer, primary_key=True, index=True)
    search_id = Column(Integer, ForeignKey("image_searches.id"))
    
    # Product information
    title = Column(String, nullable=True)
    link = Column(String, nullable=True)
    source = Column(String, nullable=True)
    price = Column(String, nullable=True)
    thumbnail = Column(String, nullable=True)
    
    # Additional metadata
    description = Column(Text, nullable=True)
    rating = Column(Float, nullable=True)
    reviews_count = Column(Integer, nullable=True)
    
    # Raw data for future reference
    raw_data = Column(Text, nullable=True)
    
    # Relationship with search
    search = relationship("ImageSearch", back_populates="results")