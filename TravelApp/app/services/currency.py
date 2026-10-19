from app.services.cache import get_cache, set_cache
import httpx

async def fetch_currency(basecurrency: str):
    cache_key = f"{basecurrency}_currency"
    cache_data = get_cache(cache_key)

    if cache_data:
        return cache_data

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://v6.exchangerate-api.com/v6/665ab8f47936d5955df1160b/latest/{basecurrency}"
        )
        response.raise_for_status()
        data = response.json()

        rates = data.get("conversion_rates", {})

        set_cache(cache_key, rates, ttl=3600)
        return rates
