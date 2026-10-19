# Travel Planner API

## Purpose
The **Travel Planner API** is a FastAPI-based backend service designed to aggregate travel information for a destination. It gathers weather forecasts, suggested places, and currency conversion rates. The API provides both standard JSON responses and a Server-Sent Events (SSE) streaming endpoint.

---

## Technology Stack
- **Python** & **FastAPI**
- **Pydantic** for request/response data models
- **httpx** for asynchronous HTTP requests
- **python-dotenv** for loading environment variables
- **Uvicorn** ASGI server (included in pinned requirements)

---

## Features and Data Sources

- **Weather Forecasts:** Fetched asynchronously from **WeatherAPI** and cached in memory for **1 hour**.
- **Currency Exchange Rates:** Fetched asynchronously from **ExchangeRate-API** and cached in memory for **1 hour**.
- **Suggested Places:** Loaded from a local, hard-coded dataset. Currently supports **Manali**, **Goa**, and **Jaipur**. Destination matching is case-insensitive and ignores surrounding whitespace.
- **Concurrent Processing:** The standard planning endpoint fetches weather, places, and currency data concurrently.
- **SSE Streaming:** The streaming endpoint sequentially fetches data and streams progress and result events via Server-Sent Events (SSE).
- **Cache Management:** Includes routes to view cache statistics and clear the in-memory cache.

---

## Configuration

The application loads environment variables from a `.env` file in the root directory:

```env
WEATHER_API_KEY=your_weather_api_key_here
CURRENCY_EXCHANGE_API_KEY=your_currency_exchange_api_key_here
```

---

## Project Structure

```text
app/
├── main.py              # Creates the FastAPI app and registers routers
├── model.py             # Pydantic models for travel requests, weather, and places
├── config.py            # Environment-variable loading
├── routes/
│   ├── planner.py       # JSON plan and cache endpoints
│   └── stream.py        # SSE plan endpoint
├── services/
│   ├── weather.py       # Weather API integration
│   ├── currency.py      # Exchange-rate API integration
│   ├── place.py         # Local place lookup
│   └── cache.py         # Simple in-memory TTL cache
└── data/
    └── places.py        # Hard-coded destination/place data
requirements.txt         # Pinned Python dependencies
```

---

## Setup and Running

1. **Install Dependencies**  
   Install the required Python packages from the pinned `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**  
   Start the local development server using Uvicorn:
   ```bash
   uvicorn app.main:app --reload
   ```

---

## Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Returns API name, version, and endpoint information. |
| `POST` | `/plan/` | Aggregates weather, places, and currency data (fetched concurrently). |
| `POST` | `/stream/plan` | Streams plan progress and results using Server-Sent Events (SSE) (fetched sequentially). |
| `GET` | `/plan/cache-stats` | Returns current in-memory cache contents and statistics. |
| `DELETE` | `/plan/cache` | Clears all data in the in-memory cache. |

 

---
### Author

 **Ayushi Singh** 
 **GitHub Profile:** https://github.com/ayus28ayushi-ai