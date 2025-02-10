import sqlite3

conn = sqlite3.connect('shop.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL,
               category TEXT NOT NULL,
               cost REAL NOT NULL,
               price REAL NOT NULL,
               quantity INTEGER NOT NULL DEFAULT 0,
               added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
               );
               """)
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               product_id INTEGER NOT NULL,
               quantity INTEGER NOT NULL,
               price REAL NOT NULL,
               sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
               FOREIGN KEY (product_id) REFERENCES products (id)
               );
               """)
cursor.execute("""
CREATE TABLE IF NOT EXISTS stock_report (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               product_id INTEGER NOT NULL,
               current_stock INTEGER NOT NULL,
               min_stock_level INTEGER NOT NULL,
               report_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
               FOREIGN KEY (product_id) REFERENCES products (id)
               );
               """)
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales_report (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               report_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
               total_sales REAL NOT NULL,
               daily_profit REAL DEFAULT 0,
               weekly_report REAL DEFAULT 0,
               monthly_profit REAL DEFAULT 0
               );
               """)
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL,
               phone TEXT UNIQUE NOT NULL,
               role TEXT NOT NULL,
               username TEXT UNIQUE NOT NULL,
               password TEXT NOT NULL,
               created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
               );
               """)
conn.commit()
conn.close()

print("Tables created successfully!")