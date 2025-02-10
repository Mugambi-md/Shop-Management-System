import sqlite3

db_path = "shop.db"
# Function to add new stock
def add_product(name, category, cost, price, quantity):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO products (name, category, cost, price, quantity) VALUES (?, ?, ?, ?, ?)",
            (name, category, cost, price, quantity),
            )
        conn.commit()
        return "Product added successfuly!"
    except sqlite3.IntegrityError:
        return "Error: Product already exists!"
    finally:
        conn.close()
# Function to update product quantity
def update_product_quantity(product_id, quantity):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT quantity FROM products WHERE id=?", (product_id))
    result = cursor.fetchone()
    if result:
        new_quantity = result[0] + quantity # Increase stock
        cursor.execute(
            "UPDATE products SET quantity=? WHERE id=?", (new_quantity, product_id)
        )
        conn.commit()
        conn.close()
        return f"Stock updated! New quantity: {new_quantity}"
    else:
        conn.close()
        return "Error: Product not found!"
# Function to view all products in stock
def view_products():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return products # Returns a list of tuples
# Function to delete a product from stock
def delete_product(product_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()
    return "Product deleted successfully!"
# Function to check low stock (compared to minimum stock level)
def check_low_stock():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""SELECT p.id, p.name, sr.current_stock, sr.min_stock_level
                   FROM products p
                   JOIN stock_report sr ON p.id=sr.product_id
                   WHERE sr.current_stock <= sr.min_stock_level
                   """)
    low_stock_items = cursor.fetchall()
    conn.close()
    return low_stock_items # Returns a list of low stock products
# Function to add stock report entry (auto-fetch current stock)
def add_stock_report(product_id, min_stock_level):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Fetch current stock from products table
    cursor.execute("SELECT quantity FROM products WHERE id=?", (product_id,))
    result = cursor.fetchone()
    if result:
        current_stock = result[0] # Get stock quantity
        cursor.execute(
            "INSERT INTO stock_report (product_id, current_stock, min_stock_level) VALUES (?, ?, ?)",
            (product_id, current_stock, min_stock_level),
        )
        conn.commit()
        conn.close()
        return f"Stock report updated! Current stock: {current_stock}, Min stock level: {min_stock_level}"
    else:
        conn.close()
        return "Error: Product not found!"