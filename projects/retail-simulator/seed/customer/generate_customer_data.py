import os
import csv
import psycopg2
from faker import Faker
import time

fake = Faker()

# PostgreSQL database configuration
db_config = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "database": os.environ.get("DB_NAME", "mydatabase"),
    "user": os.environ.get("DB_USER", "myuser"),
    "password": os.environ.get("DB_PASSWORD", "mypassword"),
    "port": os.environ.get("DB_PORT", "5432"),
}

print(db_config)
# Environment variables for controlling behaviors
output_csv = os.environ.get("OUTPUT_CSV", "True").lower() == "true"
output_sql = os.environ.get("OUTPUT_SQL", "True").lower() == "true"
insert_into_db = os.environ.get("INSERT_INTO_DB", "True").lower() == "true"

# Retrieve the NUM_RECORDS environment variable
num_records = int(os.environ.get("NUM_RECORDS", 100))  # Default to 100 if not provided

# Create a list to store customer data
customer_data = []

# Generate fake customer data
for _ in range(num_records):
    first_name = fake.first_name()
    last_name = fake.last_name()
    street = fake.street_address()
    city = fake.city()
    state = fake.state_abbr()
    postal = fake.zipcode()
    phone_number = fake.phone_number()
    email = fake.email()
    customer_as_of_date = fake.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=90)
    create_timestamp = fake.date_time_this_decade(tzinfo=None, before_now=True, after_now=False)

    customer_data.append({
        "first_name": first_name,
        "last_name": last_name,
        "street": street,
        "city": city,
        "state": state,
        "postal": postal,
        "phone_number": phone_number,
        "email": email,
        "customer_as_of_date": customer_as_of_date,
        "create_timestamp": create_timestamp,
    })

# Define the path to the CSV file
csv_file_path = f"/app/data/customers-{int(time.time() * 1000)}.csv"

# Define the path to the SQL file
sql_file_path = f"/app/data/customers-{int(time.time() * 1000)}.sql"

# Write customer data to a CSV file if enabled
if output_csv:
    with open(csv_file_path, mode="w", newline="") as file:
        fieldnames = [
            "first_name",
            "last_name",
            "street",
            "city",
            "state",
            "postal",
            "phone_number",
            "email",
            "customer_as_of_date",
            "create_timestamp",
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(customer_data)

    print(f"CSV file generated: {csv_file_path}")

# Write customer data to an SQL file if enabled
if output_sql:
    with open(sql_file_path, mode="w") as sql_file:
        sql_file.write("CREATE TABLE IF NOT EXISTS public.customers ("
                       "customer_id SERIAL PRIMARY KEY,"
                       "first_name VARCHAR(255),"
                       "last_name VARCHAR(255),"
                       "street VARCHAR(255),"
                       "city VARCHAR(255),"
                       "state VARCHAR(255),"
                       "postal VARCHAR(255),"
                       "phone_number VARCHAR(255),"
                       "email VARCHAR(255),"
                       "customer_as_of_date DATE,"
                       "create_timestamp TIMESTAMP DEFAULT current_timestamp"
                       ");\n\n")

        for customer in customer_data:
            sql_file.write(f"INSERT INTO public.customers (first_name, last_name, street, city, state, postal, phone_number, email, customer_as_of_date, create_timestamp) VALUES (")
            sql_file.write(f"'{customer['first_name']}', '{customer['last_name']}', '{customer['street']}', '{customer['city']}', '{customer['state']}', '{customer['postal']}', '{customer['phone_number']}', '{customer['email']}', '{customer['customer_as_of_date']}', '{customer['create_timestamp']}');\n")

    print(f"SQL file generated: {sql_file_path}")

# Establish a connection to the PostgreSQL database if enabled
if insert_into_db:
    try:
        connection = psycopg2.connect(**db_config)
        connection.autocommit = True
        cursor = connection.cursor()
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        exit(1)

    ctas_sql = """
	CREATE TABLE IF NOT EXISTS public.customers (
                       customer_id SERIAL PRIMARY KEY,
                       first_name VARCHAR(255),
                       last_name VARCHAR(255),
                       street VARCHAR(255),
                       city VARCHAR(255),
                       state VARCHAR(255),
                       postal VARCHAR(255),
                       phone_number VARCHAR(255),
                       email VARCHAR(255),
                       customer_as_of_date DATE,
                       create_timestamp TIMESTAMP DEFAULT current_timestamp
                       );
    """
    # Generate a single SQL INSERT statement for bulk insertion
    sql_insert = """
        INSERT INTO public.customers (
            first_name, last_name, street, city, state, postal, phone_number, email, customer_as_of_date, create_timestamp
        )
        VALUES
    """

    # Generate the values for bulk insertion
    values = []
    for customer in customer_data:
        values.append(
            f"""
            (
                '{customer['first_name']}', '{customer['last_name']}', '{customer['street']}', '{customer['city']}',
                '{customer['state']}', '{customer['postal']}', '{customer['phone_number']}', '{customer['email']}',
                '{customer['customer_as_of_date']}', '{customer['create_timestamp']}'
            )
            """
        )

    nl_char = '\n'
    # Combine the SQL statement and values for bulk insertion
    #bulk_insert_sql = f"{sql_insert}\n{',\n'.join(values)};"
    bulk_insert_sql = f"{sql_insert}\n{','.join(values)};"
    #bulk_insert_sql = f"{sql_insert}\n{',{{nl_char}}'.join(values)};"
    #bulk_insert_sql = f"{sql_insert}\n{',{chr(92)}'.join(values)};"

    # Execute the bulk SQL INSERT statement
    if output_sql:
        print("Bulk SQL INSERT statement:")
        print(bulk_insert_sql)

    if insert_into_db:
        try:
            cursor.execute(ctas_sql)
            print("CTAS completed.")
        except psycopg2.Error as e:
            print("Error executing SQL statement:", e)
        try:
            cursor.execute(bulk_insert_sql)
            print("Bulk insertion completed.")
        except psycopg2.Error as e:
            print("Error executing SQL statement:", e)
        finally:
            cursor.close()
            connection.close()
