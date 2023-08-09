# utils.py

def calculate_cart_total(cart_items):
    total = 0
    for item in cart_items:
        total += item['price'] * item['quantity']
    return total
