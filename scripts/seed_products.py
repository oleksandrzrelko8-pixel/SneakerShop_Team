import json
import os
from models import add_product, init_db, get_db_connection

SAMPLES_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'products.json')

if __name__ == '__main__':
    init_db()
    with open(SAMPLES_PATH, 'r', encoding='utf-8') as f:
        products = json.load(f)

    for p in products:
        add_product(p.get('name'), p.get('price'), p.get('image'), p.get('category'))
    print(f"Seeded {len(products)} products")