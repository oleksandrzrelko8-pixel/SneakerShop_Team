import os
import importlib


def setup_app(tmp_path):
    os.environ['DATABASE_PATH'] = str(tmp_path / 'test_api.sqlite')
    os.environ['ADMIN_TOKEN'] = 'test-token'
    os.environ['ADMIN_PASSWORD'] = 'admin123'

    import app
    importlib.reload(app)
    app.app.config['WTF_CSRF_ENABLED'] = False
    return app.app


def test_get_products_empty(tmp_path):
    app = setup_app(tmp_path)
    with app.test_client() as c:
        r = c.get('/api/products')
        assert r.status_code == 200
        assert isinstance(r.json, list)


def test_create_and_delete_product(tmp_path):
    app = setup_app(tmp_path)
    with app.test_client() as c:
        r = c.post('/api/products', json={'name': 'API Shoe', 'price': 55.5}, headers={'X-ADMIN-TOKEN': 'test-token'})
        assert r.status_code == 201
        new_id = r.json['id']

        r2 = c.get(f'/api/products/{new_id}')
        assert r2.status_code == 200 and r2.json['name'] == 'API Shoe'

        r3 = c.delete(f'/api/products/{new_id}', headers={'X-ADMIN-TOKEN': 'test-token'})
        assert r3.status_code == 200


def test_orders_via_buy(tmp_path):
    app = setup_app(tmp_path)
    with app.test_client() as c:
        # add product via admin flow
        c.post('/admin/login', data={'password': 'admin123'}, follow_redirects=True)
        c.post('/admin', data={'name': 'OrderShoe', 'price': '123', 'image': '', 'category': 'Test'}, follow_redirects=True)

        products = c.get('/api/products').json
        assert len(products) > 0
        pid = products[0]['id']

        r = c.post(f'/buy/{pid}', data={'name': 'Customer', 'phone': '+380501234567'}, follow_redirects=True)
        assert r.status_code == 200

        orders = c.get('/api/orders').json
        assert any(o['product_name'] == 'OrderShoe' for o in orders)
