from fastapi import FastAPI, Query, HTTPException
from src.models import MenuResponse, CafeMenuItem
from src.data import menu_items


app = FastAPI(
    title="Beverage Cafe Menu",
    description="Read only menu API"
)

@app.get("/")
def intro():
    return {
        "message": "Welcome to Beverages Cafe!"
    }

@app.get("/menu", response_model=MenuResponse)
def get_full_menu(category:str | None = Query(None, description="Filter by milk, fruit, matcha or coffee")):
    if category:
        filtered_items = [item for item in menu_items if item["category"] == category.lower()]
        if not filtered_items:
            raise HTTPException(status_code=404, detail=f"No item found in that category {category}")
        return MenuResponse(count=len(filtered_items), items = filtered_items)

    return MenuResponse(count=len(menu_items), items=menu_items)

@app.get("/menu/{item_id}", response_model=CafeMenuItem)
def get_item_by_id(item_id:int):
    for item in menu_items:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404,detail=f"No item found with id {item_id}" )
