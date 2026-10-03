
# Lunch Delivery System API

A REST API built with **FastAPI**, **SQLModel**, and **SQLite** to manage lunch delivery orders and track their statuses.

---
## Features
- Create and retrieve delivery orders.
- Filter orders by status and creation date.
- Support pagination.
- Generate daily order summaries by status.
- Store order data in an SQLite database.

---
## Tech Stack
- Python
- FastAPI
- SQLModel
- SQLite
- Uvicorn

---
## Setup

```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```

---
## API Documentation

Once the server is running, visit:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Health Check: http://127.0.0.1:8000/health

---
## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/order/` | Create a new order |
| GET | `/order/` | Retrieve orders with optional filters and pagination |
| GET | `/stats/daily` | Get a daily order summary |
| GET | `/health` | Check API health |

---
## Order Statuses

- `preparing`
- `picked_up`
- `in_transit`
- `delivered`

---
###  AUTHOR
 **Name:** Ayushi Singh
 **GitHub Profile:** https://github.com/ayus28ayushi-ai