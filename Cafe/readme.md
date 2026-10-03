
# Beverages Cafe Menu API

A read-only REST API built with **FastAPI** and **Pydantic** to manage and retrieve cafe menu information.

---
## Features
- Retrieve all menu items.
- Filter drinks by category (`milk`, `fruit`, `matcha`, `coffee`).
- Get a menu item by ID.
- Handle invalid requests with appropriate error responses.
---
## Tech Stack
- Python
- FastAPI
- Pydantic
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
---
## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/menu` | Get all menu items |
| GET | `/menu?category=coffee` | Filter by category |
| GET | `/menu/{item_id}` | Get an item by ID |

---
###  AUTHOR
 **Name:** Ayushi Singh
 **GitHub Profile:** https://github.com/ayus28ayushi-ai