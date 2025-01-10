import random
import datetime

# Sample data for each table
categories = [(i, f'category {i}') for i in range(1, 51)]
suppliers = [(i, f'supplier {i}', f'contact info {i}') for i in range(1, 51)]
products = []
customers = []
inventory_orders = []
inventory_order_items = []

# Generating INSERT statements for Categories
print("-- Insert categories")
for category in categories:
    print(f"INSERT INTO inventory_category (id, name) VALUES ({category[0]}, '{category[1]}');")

# Generating INSERT statements for Suppliers
print("\n-- Insert suppliers")
for supplier in suppliers:
    print(f"INSERT INTO inventory_supplier (id, name, contact_info) VALUES ({supplier[0]}, '{supplier[1]}', '{supplier[2]}');")

# Generating 150 Products
for i in range(1, 151):
    name = f'product {i}'
    category_id = random.choice(categories)[0]
    description = f'description for product {i}'
    buying_price = round(random.uniform(10.00, 500.00), 2)
    selling_price = buying_price + round(random.uniform(10.00, 100.00), 2)
    stock = random.randint(10, 500)
    supplier_id = random.choice(suppliers)[0]
    image = f'path/to/image{i}.jpg'
    products.append((i, name, category_id, description, buying_price, selling_price, stock, supplier_id, image))

# Generating INSERT statements for Products
print("\n-- Insert products")
for product in products:
    print(f"INSERT INTO inventory_product (id, name, category_id, description, buying_price, selling_price, stock, supplier_id, image) \n          VALUES ({product[0]}, '{product[1]}', {product[2]}, '{product[3]}', {product[4]}, {product[5]}, {product[6]}, {product[7]}, '{product[8]}');")

# Generating 200 Customers
for i in range(1, 201):
    name = f'customer {i}'
    phone = f'111-000-{str(i).zfill(4)}'
    address = f'address {i}'
    customers.append((i, name, phone, address))

# Generating INSERT statements for Customers
print("\n-- Insert customers")
for customer in customers:
    print(f"INSERT INTO inventory_customerinfo (id, name, phone, address) VALUES ({customer[0]}, '{customer[1]}', '{customer[2]}', '{customer[3]}');")

# Generating 200 Inventory Orders
for i in range(1, 201):
    customer_id = random.choice(customers)[0]
    order_date = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 365))
    status = random.choice(['Pending', 'Completed'])
    total_amount = round(random.uniform(50.00, 1000.00), 2)
    inventory_orders.append((i, customer_id, order_date.strftime('%Y-%m-%d %H:%M:%S'), status, total_amount))

# Generating INSERT statements for Inventory Orders
print("\n-- Insert inventory_orders")
for order in inventory_orders:
    print(f"INSERT INTO inventory_order (id, customer_id, order_date, status, total_amount) VALUES ({order[0]}, {order[1]}, '{order[2]}', '{order[3]}', {order[4]});")

# Generating 300 Inventory Order Items
for i in range(1, 301):
    order_id = random.choice(inventory_orders)[0]
    product_id = random.choice(products)[0]
    quantity = random.randint(1, 10)
    price = round(random.uniform(20.00, 500.00), 2)
    inventory_order_items.append((i, order_id, product_id, quantity, price))

# Generating INSERT statements for Inventory Order Items
print("\n-- Insert inventory_order_items")
for item in inventory_order_items:
    print(f"INSERT INTO inventory_orderitem (id, order_id, product_id, quantity, price) VALUES ({item[0]}, {item[1]}, {item[2]}, {item[3]}, {item[4]});")
