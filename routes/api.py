from flask import Blueprint, request, jsonify
from flask import Blueprint, request, jsonify
from models import get_db_connection

api_bp = Blueprint('api', __name__)

def row_to_dict(row):
        return dict(row)

# --- 1. ОТРИМАННЯ ВСІХ ТОВАРІВ ---
@api_bp.route('/api/products', methods=['GET'])
def api_get_products():
        """
        Get all products
        ---
        tags:
            - Products
        responses:
            200:
                description: List of products
        """
        conn = get_db_connection()
        products = conn.execute('SELECT * FROM products').fetchall()
        conn.close()
        return jsonify([row_to_dict(p) for p in products]), 200

# --- 2. ОТРИМАННЯ ОДНОГО ТОВАРУ ---
@api_bp.route('/api/products/<int:id>', methods=['GET'])
def api_get_product(id):
        """
        Get one product by ID
        ---
        tags:
            - Products
        parameters:
            - name: id
                in: path
                type: integer
                required: true
        responses:
            200:
                description: Product found
            404:
                description: Product not found
        """
        conn = get_db_connection()
        product = conn.execute('SELECT * FROM products WHERE id = ?', (id,)).fetchone()
        conn.close()
    
        if product is None:
                return jsonify({'error': 'Product not found'}), 404
        return jsonify(row_to_dict(product)), 200

# --- 3. СТВОРЕННЯ ТОВАРУ ---
@api_bp.route('/api/products', methods=['POST'])
def api_create_product():
        # Тільки для адміністраторів: очікуємо X-ADMIN-TOKEN заголовок або іншу зовнішню автентифікацію
        admin_token = request.headers.get('X-ADMIN-TOKEN')
        if admin_token != __import__('os').environ.get('ADMIN_TOKEN'):
            return jsonify({'error': 'Unauthorized'}), 401
        """
        Create a new product
        ---
        tags:
            - Products
        parameters:
            - in: body
                name: body
                required: true
                schema:
                    type: object
                    required:
                        - name
                        - price
                    properties:
                        name:
                            type: string
                        price:
                            type: number
        responses:
            201:
                description: Product created
        """
        data = request.get_json()
        if not data or 'name' not in data or 'price' not in data:
                return jsonify({'error': 'Bad Request'}), 400
    
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO products (name, price, image, category) VALUES (?, ?, ?, ?)',
                                 (data['name'], data['price'], data.get('image', ''), data.get('category', 'General')))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return jsonify({'id': new_id, 'message': 'Product created'}), 201

# --- 4. ВИДАЛЕННЯ ТОВАРУ ---
@api_bp.route('/api/products/<int:id>', methods=['DELETE'])
def api_delete_product(id):
        admin_token = request.headers.get('X-ADMIN-TOKEN')
        if admin_token != __import__('os').environ.get('ADMIN_TOKEN'):
            return jsonify({'error': 'Unauthorized'}), 401
        """
        Delete a product
        ---
        tags:
            - Products
        parameters:
            - name: id
                in: path
                type: integer
                required: true
        responses:
            200:
                description: Product deleted
        """
        conn = get_db_connection()
        product = conn.execute('SELECT * FROM products WHERE id = ?', (id,)).fetchone()
    
        if product is None:
                conn.close()
                return jsonify({'error': 'Product not found'}), 404
        
        conn.execute('DELETE FROM products WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Product deleted'}), 200

# --- 5. ОТРИМАННЯ ЗАМОВЛЕНЬ ---
@api_bp.route('/api/orders', methods=['GET'])
def api_get_orders():
    """
    Get all orders
    ---
    tags:
      - Orders
    responses:
      200:
        description: List of orders
    """
    conn = get_db_connection()
    query = '''
        SELECT orders.id, orders.status, orders.customer_name, products.name as product_name
        FROM orders
        JOIN products ON orders.product_id = products.id
    '''
    orders = conn.execute(query).fetchall()
    conn.close()
    return jsonify([row_to_dict(o) for o in orders]), 200
