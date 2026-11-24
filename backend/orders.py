import re


def extract_order_number(message):
    match = re.search(r"\bbk\d+\b", message, re.IGNORECASE)

    if match is None:
        return None

    return match.group().upper()


def find_order(db, order_number):
    if order_number not in db:
        return None

    order = db[order_number]

    item_texts = []
    for title, quantity in order["items"].items():
        item_texts.append(f"{title} x{quantity}")

    items_text = ", ".join(item_texts)

    return f"Order {order_number}: {order['status']}. Items: {items_text}"
