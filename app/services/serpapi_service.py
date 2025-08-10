import httpx
import json
import asyncio
import os
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.utils.deduplication import filter_duplicates
from app.utils.performance import timed_async, run_in_threadpool

# Use Redis cache in production, fallback to in-memory cache in development
if os.getenv("REDIS_ENABLED", "false").lower() == "true":
    from app.utils.redis_cache import redis_cache
    cache_decorator = redis_cache(ttl=3600)
else:
    from app.utils.performance import async_cache
    cache_decorator = async_cache(ttl=3600)

@timed_async
@cache_decorator  # Cache results for 1 hour
async def search_similar_products(image_url: str) -> List[Dict[str, Any]]:
    """
    Search for similar products using SerpAPI's Google Reverse Image Search
    
    Args:
        image_url: URL of the image to search
        
    Returns:
        List of similar products
    """
    # Construct the SerpAPI URL
    api_url = "https://serpapi.com/search.json"
    
    # Set up the query parameters
    params = {
        "engine": "google_reverse_image",
        "image_url": image_url,
        "api_key": settings.SERPAPI_API_KEY
    }
    
    # Make the API request with timeout and retries
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Try up to 3 times with exponential backoff
        for attempt in range(3):
            try:
                response = await client.get(api_url, params=params)
                
                # Check if the request was successful
                if response.status_code != 200:
                    raise Exception(f"SerpAPI request failed with status code {response.status_code}: {response.text}")
                
                # Parse the response
                data = response.json()
                
                # Extract the shopping results
                shopping_results = data.get("shopping_results", [])
                
                # Filter out duplicates using a thread pool to avoid blocking the event loop
                unique_products = await run_in_threadpool(filter_duplicates, shopping_results)
                
                # Limit to the maximum number of similar products
                return unique_products[:settings.MAX_SIMILAR_PRODUCTS]
                
            except (httpx.TimeoutException, httpx.ConnectError) as e:
                # If this is the last attempt, raise the exception
                if attempt == 2:
                    raise
                
                # Otherwise, wait and retry
                wait_time = 2 ** attempt  # Exponential backoff: 1, 2, 4 seconds
                await asyncio.sleep(wait_time)
                continue

def extract_product_info(product: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract relevant product information from SerpAPI response
    
    Args:
        product: Product data from SerpAPI
        
    Returns:
        Dictionary with extracted product information
    """
    return {
        "title": product.get("title"),
        "link": product.get("link"),
        "source": product.get("source"),
        "price": product.get("price"),
        "thumbnail": product.get("thumbnail"),
        "description": product.get("snippet"),
        "rating": product.get("rating"),
        "reviews_count": product.get("reviews"),
        "raw_data": json.dumps(product)
    }