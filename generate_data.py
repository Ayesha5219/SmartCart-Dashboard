import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)

# -----------------------------
# Customer Data
# -----------------------------

first_names = [
    "Aarav", "Ananya", "Rahul", "Priya", "Rohan",
    "Sneha", "Arjun", "Neha", "Aditya", "Ishita",
    "Karan", "Meera", "Vikram", "Pooja", "Nikhil"
]

last_names = [
    "Sharma", "Patel", "Singh", "Das", "Gupta",
    "Reddy", "Mehta", "Kumar", "Rao", "Joshi"
]

cities = [
    "Mumbai", "Delhi", "Bangalore", "Hyderabad",
    "Chennai", "Kolkata", "Pune", "Jaipur",
    "Ahmedabad", "Bhubaneswar"
]

regions = {
    "Mumbai": "West",
    "Delhi": "North",
    "Bangalore": "South",
    "Hyderabad": "South",
    "Chennai": "South",
    "Kolkata": "East",
    "Pune": "West",
    "Jaipur": "North",
    "Ahmedabad": "West",
    "Bhubaneswar": "East"
}

customers = []

for i in range(1, 101):
    name = random.choice(first_names) + " " + random.choice(last_names)
    city = random.choice(cities)

    customers.append({
        "Customer_ID": f"CUST{i:03d}",
        "Customer_Name": name,
        "City": city,
        "Region": regions[city],
        "Customer_Type": random.choice(["New", "Returning"])
    })

customers_df = pd.DataFrame(customers)

customers_df.to_csv("data/customers.csv", index=False)


# -----------------------------
# Product Data
# -----------------------------

products = [
    ("Laptop", "Electronics", 65000),
    ("Smartphone", "Electronics", 30000),
    ("Headphones", "Electronics", 3000),
    ("Smart Watch", "Electronics", 7000),
    ("Keyboard", "Electronics", 2500),
    ("Office Chair", "Furniture", 8500),
    ("Study Table", "Furniture", 6000),
    ("Backpack", "Accessories", 1800),
    ("Running Shoes", "Fashion", 4000),
    ("T-Shirt", "Fashion", 1200),
    ("Jeans", "Fashion", 2500),
    ("Coffee Maker", "Home & Kitchen", 5000),
    ("Mixer Grinder", "Home & Kitchen", 4500),
    ("Water Bottle", "Home & Kitchen", 800),
    ("Notebook", "Stationery", 300)
]


# -----------------------------
# Order Data
# -----------------------------

orders = []

start_date = datetime(2026, 1, 1)

for i in range(1, 1001):

    customer = random.choice(customers)

    product, category, price = random.choice(products)

    quantity = random.randint(1, 5)

    order_date = start_date + timedelta(
        days=random.randint(0, 364)
    )

    revenue = price * quantity

    cost = revenue * random.uniform(0.55, 0.80)

    profit = revenue - cost

    orders.append({
        "Order_ID": f"ORD{i:04d}",
        "Order_Date": order_date.strftime("%Y-%m-%d"),
        "Customer_ID": customer["Customer_ID"],
        "Product": product,
        "Category": category,
        "Region": customer["Region"],
        "Quantity": quantity,
        "Price": price,
        "Revenue": round(revenue, 2),
        "Cost": round(cost, 2),
        "Profit": round(profit, 2),
        "Payment_Method": random.choice([
            "Credit Card",
            "Debit Card",
            "UPI",
            "Cash on Delivery",
            "Net Banking"
        ])
    })

orders_df = pd.DataFrame(orders)

orders_df.to_csv("data/orders.csv", index=False)

print("Data generation completed successfully!")
print("Created: data/customers.csv")
print("Created: data/orders.csv")
print(f"Customers: {len(customers_df)}")
print(f"Orders: {len(orders_df)}")