import os
import mysql.connector
import psycopg2

# Extract from MySQL
print("Connecting to MySQL...")
mysql_conn = mysql.connector.connect(
    host=os.getenv('MYSQL_HOST', 'mysql'),
    user=os.getenv('MYSQL_USER', 'etl_user'),
    password=os.getenv('MYSQL_PASSWORD', 'etl_password'),
    database=os.getenv('MYSQL_DB', 'source_db')
)
mysql_cursor = mysql_conn.cursor(dictionary=True)

print("Extracting data...")
mysql_cursor.execute("SELECT * FROM sales")
data = mysql_cursor.fetchall()
print(f"Extracted {len(data)} rows")
mysql_cursor.close()
mysql_conn.close()

# Transform - calculate total amount
print("Transforming data...")
for row in data:
    row['total_amount'] = float(row['price']) * row['quantity']
    print(f"  {row['product']}: ${row['total_amount']}")

# Load to PostgreSQL
print("Connecting to PostgreSQL...")
pg_conn = psycopg2.connect(
    host=os.getenv('POSTGRES_HOST', 'postgres'),
    user=os.getenv('POSTGRES_USER', 'warehouse_user'),
    password=os.getenv('POSTGRES_PASSWORD', 'warehouse_pass'),
    database=os.getenv('POSTGRES_DB', 'warehouse_db')
)
pg_cursor = pg_conn.cursor()

# Create table
print("Creating table...")
pg_cursor.execute("""
    CREATE TABLE IF NOT EXISTS raw_data (
        id INT PRIMARY KEY,
        product VARCHAR(100),
        price DECIMAL(10,2),
        quantity INT,
        sale_date DATE,
        total_amount DECIMAL(10,2)
    )
""")

# Clear old data
pg_cursor.execute("TRUNCATE TABLE raw_data")

# Insert data
print("Loading data...")
for row in data:
    pg_cursor.execute("""
        INSERT INTO raw_data (id, product, price, quantity, sale_date, total_amount)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (row['id'], row['product'], row['price'], row['quantity'], 
          row['sale_date'], row['total_amount']))

pg_conn.commit()
print(f"Loaded {len(data)} rows to PostgreSQL")

pg_cursor.close()
pg_conn.close()
print("ETL Complete!")
