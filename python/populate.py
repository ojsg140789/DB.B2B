# python/populate.py

import json
import psycopg2
import bcrypt
from datetime import datetime

# Database connection parameters
db_config = {
    "dbname": "b2b",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432,
}

def hashPassword(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def populateUserTable(cursor):
    username = "user@gmail.com"
    password = "user123"
    hashedPassword = hashPassword(password)

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s) ON CONFLICT DO NOTHING",
        (username, hashedPassword)
    )
    print("User table populated.")

def populateOrdersTable(cursor):
    with open("/data/db.json", "r") as file:
        orders = json.load(file)

    for order in orders:
        # Parse and format the fields from JSON
        id = order.get("id")
        createdAt = order.get("createdAt", datetime.utcnow())
        updatedAt = order.get("updatedAt", datetime.utcnow())
        deletedAt = order.get("deletedAt")  # Can be None
        date = order["date"]
        status = order["status"]
        price = order["price"]
        loanId = order["loanId"]
        merchantId = order["merchantId"]
        products = order.get("products")  # Can be None
        branchId = order["branchId"]
        sellsAgentId = order["sellsAgentId"]

        # Convert date fields to a datetime object if they are in string format
        createdAt = createdAt if isinstance(createdAt, datetime) else datetime.fromisoformat(createdAt)
        updatedAt = updatedAt if isinstance(updatedAt, datetime) else datetime.fromisoformat(updatedAt)
        date = date if isinstance(date, datetime) else datetime.fromisoformat(date.split(" ")[0])

        # Insert into orders table, using 'id' only if it's provided
        if id:
            cursor.execute(
                """
                INSERT INTO orders (id, createdAt, updatedAt, deletedAt, date, status, price, loanId, 
                merchantId, products, branchId, sellsAgentId)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    id,
                    createdAt,
                    updatedAt,
                    deletedAt,
                    date,
                    status,
                    price,
                    loanId,
                    merchantId,
                    products,
                    branchId,
                    sellsAgentId
                )
            )
        else:
            cursor.execute(
                """
                INSERT INTO orders (createdAt, updatedAt, deletedAt, date, status, price, loanId, 
                merchantId, products, branchId, sellsAgentId)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    createdAt,
                    updatedAt,
                    deletedAt,
                    date,
                    status,
                    price,
                    loanId,
                    merchantId,
                    products,
                    branchId,
                    sellsAgentId
                )
            )
    print("Orders table populated.")

def main():
    conn = None
    try:
        conn = psycopg2.connect(**db_config)
        conn.autocommit = True
        cursor = conn.cursor()

        populateUserTable(cursor)
        populateOrdersTable(cursor)

        cursor.close()
        print("Database populated successfully.")
    except Exception as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    main()
