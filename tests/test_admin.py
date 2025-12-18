import os
from app import app
# Disable CSRF for tests
app.config['WTF_CSRF_ENABLED'] = False


def test_admin_login_and_access():
    with app.test_client() as c:
        resp = c.post('/admin/login', data={'password': os.environ.get('ADMIN_PASSWORD', 'admin123')}, follow_redirects=True)
        assert resp.status_code == 200
        # after login we can access admin panel
        r2 = c.get('/admin')
        assert r2.status_code == 200
