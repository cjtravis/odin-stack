import psycopg2
from faker import Faker
import random
import time

# PostgreSQL database configuration
db_config = {
    "host": "192.168.0.203",  # This is the hostname of the PostgreSQL container
    "database": "posdb",  # Your database name
    "user": "postgres",  # Your PostgreSQL username
    "password": "password",  # Your PostgreSQL password
    "port": 55432
}

fake = Faker()

def create_connection():
    try:
        connection = psycopg2.connect(**db_config)
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)
        return None

def generate_pos_data(connection):
    cursor = connection.cursor()
    while True:  # Run indefinitely
        product_name = fake.word()
        price = round(random.uniform(1, 100), 2)
        quantity = random.randint(1, 10)
        total_amount = round(price * quantity, 2)
        timestamp = fake.date_time_between(start_date="-30d", end_date="now").strftime("%Y-%m-%d %H:%M:%S")

        insert_query = f"""
            INSERT INTO orders (product_name, price, quantity, total_amount)
            VALUES ('{product_name}', {price}, {quantity}, {total_amount})
        """
        cursor.execute(insert_query)
        connection.commit()

        # Print a human-readable message after each successful insert
        print(f"Order: {product_name}, Price: ${price:.2f}, Quantity: {quantity}, Total Amount: ${total_amount:.2f}")
        sleep_window = random.uniform(1, 10)
        time.sleep(sleep_window)  # Adjust the sleep duration as needed

if __name__ == "__main__":
    connection = create_connection()
    if connection:
        generate_pos_data(connection)
