-- init.sql
-- Create the "product" table if it doesn't exist
CREATE TABLE IF NOT EXISTS product (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255),
    category VARCHAR(255),
    brand VARCHAR(255),
    vendor VARCHAR(255),
    price DECIMAL(10, 2),
    release_date DATE,
    upc bigint
);

-- Create the "orders" table
CREATE TABLE IF NOT EXISTS public.orders (
    order_id SERIAL PRIMARY KEY,
    product_id INT,
    price DECIMAL(10, 2),
    quantity INT,
    total_amount DECIMAL(10, 2),
    status VARCHAR(255),
    created_at TIMESTAMP DEFAULT current_timestamp,
    FOREIGN KEY (product_id) REFERENCES public.product(product_id)
);


-- Insert product data
INSERT INTO product (product_name, category, brand, vendor, price, release_date, upc)
VALUES
    ('LED Smart TV', 'Electronics', 'Samsung', 'Electronics Store', 499.99, '2023-01-15', '123456789012'),
    ('Wireless Bluetooth Headphones', 'Electronics', 'Sony', 'Electronics Store', 149.99, '2023-02-10', '234567890123'),
    ('Stainless Steel Refrigerator', 'Appliances', 'Whirlpool', 'Appliance Center', 799.00, '2022-12-20', '345678901234'),
    ('Leather Sofa', 'Furniture', 'Ashley Furniture', 'Furniture Warehouse', 899.99, '2023-01-05', '456789012345'),
    ('4-Burner Gas Range', 'Appliances', 'GE Appliances', 'Appliance Center', 599.00, '2023-02-01', '567890123456'),
    ('Apple iPhone 13', 'Electronics', 'Apple', 'Electronics Store', 799.00, '2022-09-24', '678901234567'),
    ('Queen Size Mattress', 'Furniture', 'Sealy', 'Furniture Warehouse', 499.99, '2023-01-10', '789012345678'),
    ('DSLR Camera Kit', 'Electronics', 'Canon', 'Electronics Store', 799.99, '2022-11-30', '890123456789'),
    ('Coffee Maker', 'Appliances', 'Keurig', 'Appliance Center', 99.99, '2023-02-15', '901234567890'),
    ('Men''s Dress Shoes', 'Apparel', 'Nike', 'Shoe Store', 79.99, '2023-03-01', '012345678901'),
    ('Washing Machine', 'Appliances', 'LG Appliances', 'Appliance Center', 649.00, '2022-11-15', '1234567890123'),
    ('55-Inch 4K UHD TV', 'Electronics', 'LG', 'Electronics Store', 549.99, '2022-12-10', '2345678901234'),
    ('Microwave Oven', 'Appliances', 'Panasonic', 'Appliance Center', 129.00, '2023-02-25', '3456789012345'),
    ('Gaming Laptop', 'Electronics', 'MSI', 'Electronics Store', 1399.99, '2022-11-05', '4567890123456'),
    ('Women''s Handbag', 'Fashion', 'Coach', 'Department Store', 199.99, '2023-01-20', '5678901234567'),
    ('Blender', 'Appliances', 'Vitamix', 'Appliance Center', 299.99, '2023-02-20', '6789012345678'),
    ('Outdoor Patio Furniture Set', 'Furniture', 'Hampton Bay', 'Furniture Warehouse', 899.00, '2022-12-05', '7890123456789'),
    ('Fitness Tracker Watch', 'Electronics', 'Fitbit', 'Electronics Store', 149.99, '2022-10-20', '8901234567890'),
    ('Portable Air Conditioner', 'Appliances', 'Honeywell', 'Appliance Center', 399.00, '2022-11-10', '0123456789012'),
    ('Children''s Bicycle', 'Sporting Goods', 'Schwinn', 'Sports Store', 149.99, '2023-03-05', '12345678901234'),
    ('Hair Dryer', 'Appliances', 'Conair', 'Appliance Center', 49.99, '2023-03-10', '23456789012345'),
    ('Electric Kettle', 'Appliances', 'Breville', 'Appliance Center', 79.99, '2023-01-25', '34567890123456'),
    ('Soundbar Speaker', 'Electronics', 'Bose', 'Electronics Store', 249.99, '2022-12-15', '45678901234567'),
    ('Baby Stroller', 'Baby & Kids', 'Graco', 'Baby Store', 199.99, '2023-01-15', '56789012345678'),
    ('Espresso Machine', 'Appliances', 'De''Longhi', 'Appliance Center', 299.00, '2022-10-10', '67890123456789'),
    ('Gaming Console (PlayStation 5)', 'Electronics', 'Sony', 'Electronics Store', 499.99, '2022-11-20', '78901234567890'),
    ('Laptop Backpack', 'Electronics', 'SwissGear', 'Electronics Store', 49.99, '2023-01-30', '01234567890123'),
    ('Toaster Oven', 'Appliances', 'Black & Decker', 'Appliance Center', 69.99, '2023-02-05', '123456789012345'),
    ('Wireless Mouse', 'Electronics', 'Logitech', 'Electronics Store', 29.99, '2023-01-05', '234567890123456');
