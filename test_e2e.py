from app import app
from models import get_all_products, get_all_orders


def run_test():
    with app.test_client() as c:
        # 1) Add a product via admin POST
        resp = c.post('/admin', data={
            'name': 'E2E Shoe',
            'price': '1234.5',
            'image': '',
            'category': 'E2E'
        }, follow_redirects=True)
        print('Add product status:', resp.status_code)

        products = get_all_products()
        print('Products now:', [p['name'] for p in products])
        # Find our product
        pid = None
        for p in products:
            if p['name'] == 'E2E Shoe':
                pid = p['id']
                break
        if pid is None:
            print('ERROR: Product not found')
            return

        # 2) Visit buy page (GET)
        r = c.get(f'/buy/{pid}')
        print('/buy GET status:', r.status_code)

        # 3) Submit order
        r2 = c.post(f'/buy/{pid}', data={'name': 'Test Client', 'phone': '+380501234567'}, follow_redirects=True)
        print('/buy POST status:', r2.status_code)

        # 4) Verify orders exist
        orders = get_all_orders()
        print('Orders count:', len(orders))
        if orders:
            latest = orders[0]
            print('Latest order:', dict(latest))
            assert latest['product_name'] == 'E2E Shoe', 'Product name mismatch in order'
            assert latest['customer_phone'] == '+380501234567', 'Phone mismatch'
            print('E2E test passed')
        else:
            print('No orders found - test failed')


if __name__ == '__main__':
    run_test()
