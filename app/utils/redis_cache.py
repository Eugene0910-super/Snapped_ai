import redis
import json
import functools
import time
import os
from typing import Any, Callable, Dict, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check if Redis is available
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
REDIS_ENABLED = os.getenv("REDIS_ENABLED", "false").lower() == "true"

# Initialize Redis client if enabled
redis_client = None
if REDIS_ENABLED:
    try:
        redis_client = redis.from_url(REDIS_URL)
        redis_client.ping()  # Test connection
        logger.info("Redis cache enabled")
    except redis.ConnectionError:
        logger.warning("Failed to connect to Redis, falling back to in-memory cache")
        redis_client = None
        REDIS_ENABLED = False

# In-memory cache as fallback
_memory_cache: Dict[str, Dict[str, Any]] = {}

def redis_cache(ttl: int = 3600):
    """
    Cache decorator that uses Redis if available, otherwise falls back to in-memory cache
    
    Args:
        ttl: Time to live in seconds (default: 1 hour)
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Create a cache key from function name and arguments
            key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Try to get from cache
            if REDIS_ENABLED and redis_client:
                cached_data = redis_client.get(key)
                if cached_data:
                    logger.info(f"Redis cache hit for {func.__name__}")
                    return json.loads(cached_data)
            elif key in _memory_cache:
                entry = _memory_cache[key]
                if time.time() - entry["timestamp"] < ttl:
                    logger.info(f"Memory cache hit for {func.__name__}")
                    return entry["result"]
            
            # Execute the function
            result = await func(*args, **kwargs)
            
            # Cache the result
            try:
                if REDIS_ENABLED and redis_client:
                    redis_client.setex(key, ttl, json.dumps(result))
                else:
                    _memory_cache[key] = {
                        "result": result,
                        "timestamp": time.time()
                    }
            except Exception as e:
                logger.error(f"Error caching result: {str(e)}")
            
            return result
        return wrapper
    return decorator

def clear_cache():
    """
    Clear the cache
    """
    if REDIS_ENABLED and redis_client:
        redis_client.flushdb()
        logger.info("Redis cache cleared")
    else:
        global _memory_cache
        _memory_cache = {}
        logger.info("Memory cache cleared")