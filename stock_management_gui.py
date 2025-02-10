import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from stock_management import add_product, update_product_quantity, view_products, delete_product, check_low_stock, add_stock_report

stock_tree = None # Define stock tree as a global variable

def refresh_stock():
    """Refresh the product list."""
    global stock_tree
    if stock_tree:
        for row in stock_tree.get_children():
            stock_tree.delete(row)
        products = view_products()
        for product in products:
            stock_tree.insert("", "end", values=product)

def add_new_product():
    """Dialog to add a new product."""
    name = simpledialog.askstring("Add Product", "Enter product name:")
    category = simpledialog.askstring("Add Product", "Enter product category:")
    cost = simpledialog.askfloat("Add Product", "Enter cost Price:")
    price = simpledialog.askfloat("Add Product", "Enter selling price:")
    quantity = simpledialog.askinteger("Add Product", "Enter quantity:")

    if None in [name, category, cost, price, quantity]:
        messagebox.showerror("Error", "All Fields Are Required!")
        return
    result = add_product(name, category, cost, price, quantity)
    messagebox.showinfo("Add Product", result)
    refresh_stock()

def update_stock():
    """Update product quantity."""
    selected = stock_tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select a product to update stock.")
        return
    product_id = stock_tree.item(selected, "values")[0]
    quantity = simpledialog.askinteger("Update Stock", "Enter quantity to add!")
    if quantity is None:
        return
    result = update_product_quantity(product_id, quantity)
    messagebox.showinfo("Update Stock", result)
    refresh_stock()

def remove_product():
    """Delete a selected product."""
    selected = stock_tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select a product to delete.")
        return
    product_id = stock_tree.item(selected, "values")[0]
    confirm = messagebox.askyesno("Delete Product", "Are you sure you want to delete this product?")
    if confirm:
        result = delete_product(product_id)
        messagebox.showinfo("Delete Product", result)
        refresh_stock()

def check_stock_levels():
    """Check low stock items."""
    low_stock_items = check_low_stock()
    if not low_stock_items:
        messagebox.showinfo("Low Stock", "All products are above minimum stock level.")
    else:
        stock_list ="\n".join([f"{item[1]} - Current: {item[2]}, Min: {item[3]}" for item in low_stock_items])
        messagebox.showwarning("Low Stock Items", stock_list)

def add_min_stock_level():
    """Set a minimum stock level for a product."""
    selected = stock_tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select a product to set min stock level.")
        return
    product_id = stock_tree.item(selected, "values")[0]
    min_stock_level = simpledialog.askinteger("Min Stock Level", "Enter minimum stock level:")
    if min_stock_level is None:
        return
    result = add_stock_report(product_id, min_stock_level)
    messagebox.showinfo("Stock Report", result)
    refresh_stock()

# Create stock management window
def open_stock_management_window():
    global stock_tree # Use global stock tree so it can be accessed elsewhere
    stock_window = tk.Toplevel()
    stock_window.title("Stock Management")
    stock_window.geometry("800x500")
# Frame for stock list
    frame_left = tk.Frame(stock_window)
    frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
# Treeview for stock display
    columns = ("ID", "Name", "Category", "Cost", "Price", "Quantity", "Added Date")
    stock_tree = ttk.Treeview(frame_left, columns=columns, show="headings")
    for col in columns:
        stock_tree.heading(col, text=col)
        stock_tree.column(col, width=100)
    stock_tree.pack(fill=tk.BOTH, expand=True)
    refresh_stock()
# Frame for buttons
    frame_right = tk.Frame(stock_window)
    frame_right.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
# Buttons for stock actions
    tk.Button(frame_right, text="Add Product", command=add_new_product, width=20).pack(pady=5)
    tk.Button(frame_right, text="Update Stock", command=update_stock, width=20).pack(pady=5)
    tk.Button(frame_right, text="Check Low Stock", command=check_stock_levels, width=20).pack(pady=5)
    tk.Button(frame_right, text="Set Stock Level", command=add_min_stock_level, width=20).pack(pady=5)
    tk.Button(frame_right, text="Delete Product", command=remove_product, width=20).pack(pady=5)
    tk.Button(frame_right, text="Close", command=stock_window.destroy, width=20).pack(pady=5)
# Run the window
    stock_window.mainloop()