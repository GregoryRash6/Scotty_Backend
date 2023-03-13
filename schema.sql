CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    size TEXT,
    quantity INTEGER NOT NULL
);