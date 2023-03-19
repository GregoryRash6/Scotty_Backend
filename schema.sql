CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    name TEXT,
    price DECIMAL(10,2),
    size TEXT,
    quantity INTEGER,
    image_url TEXT,
    sku TEXT,
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER,
    product_id INTEGER,
    address_id INTEGER,
    ordered_at TIME
);

CREATE TABLE address (
    id SERIAL PRIMARY KEY,
    address_1 TEXT,
    address_2 TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT
);

CREATE TABLE seller (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER,
    name TEXT
);

CREATE TABLE customer (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    name TEXT,
    default_address TEXT,
    email TEXT,
    phone TEXT
);