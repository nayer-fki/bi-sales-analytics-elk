import random
import json
from datetime import datetime, timedelta
from collections import defaultdict

random.seed(42)

CITIES = ["Tunis", "Sfax", "Sousse", "Bizerte", "Nabeul", "Ariana", "Gabes"]
CATEGORIES = ["Electronics", "Fashion", "Home", "Beauty", "Sports", "Books", "Food"]
DEVICES = ["mobile", "desktop", "tablet"]
CHANNELS = ["google", "facebook", "instagram", "direct", "email"]

def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days),
                             seconds=random.randint(0, 86400))

def gen_customers(n=10000):
    start = datetime(2022, 1, 1)
    end = datetime(2024, 12, 31)
    customers = []
    for i in range(1, n + 1):
        customers.append({
            "customer_id": i,
            "age": random.randint(18, 65),
            "city": random.choice(CITIES),
            "signup_date": random_date(start, end).isoformat()
        })
    return customers

def gen_products(n=500):
    products = []
    for i in range(1, n + 1):
        category = random.choice(CATEGORIES)
        base_price = {
            "Electronics": (200, 5000),
            "Fashion": (20, 500),
            "Home": (30, 1200),
            "Beauty": (10, 300),
            "Sports": (15, 800),
            "Books": (5, 120),
            "Food": (2, 80),
        }[category]
        price = round(random.uniform(*base_price), 2)

        products.append({
            "product_id": i,
            "category": category,
            "price": price,
            "name": f"{category} Product {i}"
        })
    return products

def gen_sales(customers_count=10000, products_count=500, n=200000):
    start = datetime(2023, 1, 1)
    end = datetime(2024, 12, 31)
    sales = []
    for i in range(1, n + 1):
        customer_id = random.randint(1, customers_count)
        product_id = random.randint(1, products_count)

        qty = random.randint(1, 5)
        unit_price = round(random.uniform(5, 5000), 2)
        amount = round(unit_price * qty, 2)

        sales.append({
            "sale_id": i,
            "customer_id": customer_id,
            "product_id": product_id,
            "quantity": qty,
            "amount": amount,
            "sale_date": random_date(start, end).isoformat()
        })
    return sales

# ✅ NEW: events generator (click/view/purchase)
def gen_events(customers_count=10000, products_count=500, n=400000):
    start = datetime(2023, 1, 1)
    end = datetime(2024, 12, 31)

    # Weights: views more than clicks, clicks more than purchases
    event_types = ["view", "click", "add_to_cart", "purchase"]
    weights = [0.55, 0.30, 0.10, 0.05]

    events = []
    for i in range(1, n + 1):
        customer_id = random.randint(1, customers_count)
        product_id = random.randint(1, products_count)
        e_type = random.choices(event_types, weights=weights, k=1)[0]

        events.append({
            "event_id": i,
            "customer_id": customer_id,
            "product_id": product_id,
            "event_type": e_type,
            "event_date": random_date(start, end).isoformat(),
            "device": random.choice(DEVICES),
            "channel": random.choice(CHANNELS),
            "session_id": f"s{random.randint(1, 150000)}"
        })
    return events

# ✅ NEW: customer metrics from events (frequency)
def gen_customer_metrics(events, customers_count=10000):
    stats = defaultdict(lambda: {"views": 0, "clicks": 0, "add_to_cart": 0, "purchases": 0, "last": None})

    for e in events:
        cid = e["customer_id"]
        et = e["event_type"]
        if et == "view":
            stats[cid]["views"] += 1
        elif et == "click":
            stats[cid]["clicks"] += 1
        elif et == "add_to_cart":
            stats[cid]["add_to_cart"] += 1
        elif et == "purchase":
            stats[cid]["purchases"] += 1

        # last activity
        dt = e["event_date"]
        if stats[cid]["last"] is None or dt > stats[cid]["last"]:
            stats[cid]["last"] = dt

    metrics = []
    for cid in range(1, customers_count + 1):
        s = stats[cid]
        total_events = s["views"] + s["clicks"] + s["add_to_cart"] + s["purchases"]

        # frequency_score: events per month (approx over 24 months)
        frequency_score = round(total_events / 24, 2)

        metrics.append({
            "customer_id": cid,
            "total_views": s["views"],
            "total_clicks": s["clicks"],
            "total_add_to_cart": s["add_to_cart"],
            "total_purchases": s["purchases"],
            "total_events": total_events,
            "frequency_score": frequency_score,
            "last_activity_date": s["last"]
        })
    return metrics

def write_jsonl(path, docs):
    with open(path, "w", encoding="utf-8") as f:
        for d in docs:
            f.write(json.dumps(d) + "\n")

if __name__ == "__main__":
    customers = gen_customers(10000)
    products  = gen_products(500)
    sales     = gen_sales(10000, 500, 200000)

    # ✅ New BI events
    events    = gen_events(10000, 500, 400000)
    metrics   = gen_customer_metrics(events, 10000)

    write_jsonl("data/customers.jsonl", customers)
    write_jsonl("data/products.jsonl", products)
    write_jsonl("data/sales.jsonl", sales)
    write_jsonl("data/events.jsonl", events)
    write_jsonl("data/customer_metrics.jsonl", metrics)

    print("Done ✅ Generated:")
    print(" - data/customers.jsonl")
    print(" - data/products.jsonl")
    print(" - data/sales.jsonl")
    print(" - data/events.jsonl")
    print(" - data/customer_metrics.jsonl")
