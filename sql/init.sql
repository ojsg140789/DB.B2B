-- sql/init.sql

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);

-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deletedAt TIMESTAMP,
    date TIMESTAMP NOT NULL,
    status VARCHAR(50) NOT NULL,
    price DECIMAL(18, 2) NOT NULL,
    loanId INTEGER NOT NULL,
    merchantId INTEGER NOT NULL,
    products TEXT,
    branchId INTEGER NOT NULL,
    sellsAgentId INTEGER NOT NULL
);
