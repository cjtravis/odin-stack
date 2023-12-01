import os
import csv
from faker import Faker
import random

fake = Faker()

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
csv_file_path = "/app/data/customers.csv"

# Write customer data to a CSV file
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
