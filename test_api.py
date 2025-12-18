from app import app
# Disable CSRF for test client
app.config['WTF_CSRF_ENABLED'] = False
import json


def run_api_smoke():
    with app.test_client() as c:
        # 1) GET all products
        r = c.get('/api/products')
        print('/api/products GET', r.status_code)

        # 2) POST create product (вимагає заголовку X-ADMIN-TOKEN)
        import os
        token = os.environ.get('ADMIN_TOKEN', 'admin-token')
        payload = {'name': 'API Shoe', 'price': 777.0, 'category': 'API'}
        r2 = c.post('/api/products', data=json.dumps(payload), content_type='application/json', headers={'X-ADMIN-TOKEN': token})
        print('/api/products POST', r2.status_code, r2.json)
        new_id = r2.json.get('id')

        # 3) GET product by id
        r3 = c.get(f'/api/products/{new_id}')
        print(f'/api/products/{new_id} GET', r3.status_code, r3.json)

        # 4) DELETE product
        r5 = c.delete(f'/api/products/{new_id}')
        print('DELETE', r5.status_code, r5.json)

        # 6) GET orders
        r6 = c.get('/api/orders')
        print('/api/orders GET', r6.status_code, 'count=', len(r6.json))


if __name__ == '__main__':
    run_api_smoke()
