# inventory_service.py

from fastapi import FastAPI

app = FastAPI()

# Simulated inventory data (you may replace this with a database)
inventory = {
    1: {"product_id": 1, "quantity": 10},
    2: {"product_id": 2, "quantity": 15},
    # Add more products and quantities as needed
}

@app.get("/inventory/{product_id}")
async def get_product_inventory(product_id: int):
    return {"product_id": product_id, "quantity": inventory.get(product_id, {}).get("quantity", 0)}

@app.post("/inventory/{product_id}/decrement")
async def decrement_inventory(product_id: int, quantity: int):
    if product_id in inventory and inventory[product_id]["quantity"] >= quantity:
        inventory[product_id]["quantity"] -= quantity
        return {"message": f"Stock decremented for product {product_id} by {quantity} units"}
    else:
        return {"error": "Insufficient stock"}
