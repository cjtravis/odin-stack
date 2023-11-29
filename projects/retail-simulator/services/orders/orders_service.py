from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from datetime import datetime
import random
import requests

app = FastAPI()

# PostgreSQL database configuration
db_config = {
    "host": "192.168.0.203",
    "database": "posdb",
    "user": "postgres",
    "password": "password",
    "port": 55432,
}

# Data models
class OrderCreate(BaseModel):
    product_id: int
    quantity: int
#    status: str

class Order(BaseModel):
    order_id: int
    product_id: int
    price: float
    quantity: int
    total_amount: float
    created_at: datetime
    status: str

# Create a database connection pool
conn = psycopg2.connect(**db_config)
conn.autocommit = True

# URL of the inventory_service
inventory_service_url = "http://192.168.0.203:8001"  # Assuming a Docker network setup

# Service logic for CRUD operations
@app.post("/orders/", response_model=Order)
async def create_order(order: OrderCreate):
    cursor = conn.cursor()
    try:
        # Get product details including price
        cursor.execute("SELECT product_id, price FROM product WHERE product_id = %s;", (order.product_id,))
        product_data = cursor.fetchone()

        if product_data:
            product_id, price = product_data
            total_amount = price * order.quantity
            timestamp = datetime.now()
            status = "Open"

            # Check inventory availability using the inventory service
            inventory_check_url = "{isurl}/inventory/{product_id}".format(isurl=inventory_service_url,product_id=order.product_id)
            inventory_response = requests.get(inventory_check_url)

            if inventory_response.status_code == 200:
                current_quantity = inventory_response.json()["quantity"]
                if current_quantity >= order.quantity:
                    # Proceed with placing the order
                    # Insert the order into the database
                    cursor.execute(
                        """
                        INSERT INTO public.orders (product_id, price, quantity, total_amount, created_at, status)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        RETURNING order_id;
                        """,
                        (order.product_id, price, order.quantity, total_amount, timestamp, status),
                    )
                    order_id = cursor.fetchone()[0]

                    # Decrement the inventory using the inventory service
                    decrement_inventory_url = "{isurl}/inventory/{product_id}/decrement".format(
                        isurl=inventory_service_url,
                        product_id=order.product_id
                    )
                    decrement_response = requests.post(decrement_inventory_url, json={"quantity": order.quantity})

                    if decrement_response.status_code == 200:
                        return {
                            "order_id": order_id,
                            "product_id": order.product_id,
                            "price": price,
                            "quantity": order.quantity,
                            "total_amount": total_amount,
                            "created_at": timestamp,
                            "status": status,
                        }
                    else:
                        raise HTTPException(status_code=500, detail="Failed to decrement inventory")
                else:
                    raise HTTPException(status_code=400, detail="Insufficient stock")
            else:
                raise HTTPException(status_code=500, detail="Failed to check inventory")

        else:
            raise HTTPException(status_code=404, detail="Product not found")

    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail="Database error")

@app.get("/orders/{order_id}", response_model=Order)
async def read_order(order_id: int):
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT
                o.order_id,
                o.product_id,
                p.price,
                o.quantity,
                o.total_amount,
                o.created_at,
                o.status  -- Remove 'upc' from the query
            FROM public.orders o
            JOIN product p ON o.product_id = p.product_id
            WHERE o.order_id = %s;
            """,
            (order_id,),
        )
        order_data = cursor.fetchone()

        if order_data:
            (
                order_id,
                product_id,
                price,
                quantity,
                total_amount,
                created_at,
                status,
            ) = order_data
            return {
                "order_id": order_id,
                "product_id": product_id,
                "price": price,
                "quantity": quantity,
                "total_amount": total_amount,
                "created_at": created_at,
                "status": status,
            }
        else:
            raise HTTPException(status_code=404, detail="Order not found")

    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail="Database error")

