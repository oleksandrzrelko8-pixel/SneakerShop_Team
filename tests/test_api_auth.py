from app import app

# Disable CSRF for tests
app.config['WTF_CSRF_ENABLED'] = False


def test_api_create_requires_token():
    with app.test_client() as c:
        resp = c.post('/api/products', json={'name': 'NoAuth', 'price': 1.0})
        assert resp.status_code == 401


def test_api_delete_requires_token():
    with app.test_client() as c:
        resp = c.delete('/api/products/1')
        assert resp.status_code == 401
