from datetime import datetime
from datetime import timedelta

# we are trying to implement a simple in-memory cache

cache = {}

# function to get the cache
def get_cache(key: str) ->dict | None:
    if key not in cache:
        return None

    entry = cache[key]
    if timedelta(seconds=entry['ttl']) < (datetime.now() - entry["created_at"]):
        del cache[key]
        return None
    
    return entry["data"]

# function to set a cache
def set_cache(
        key: str,
        data:dict,
        ttl: int
) -> None:
    cache[key] = {
        "data": data,
        "created_at": datetime.now(),
        "ttl": ttl
    }


# function to clear the cache
def clear_cache() -> None:
    cache.clear()

def get_all_cache():
    return cache