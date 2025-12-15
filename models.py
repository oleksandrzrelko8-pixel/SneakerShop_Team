import sqlite3

def get_db_connection():
    conn = sqlite3.connect('db.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    # 1. Відгуки
    c.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            rating INTEGER DEFAULT 5
        )
    ''')
    
    # 2. Товари
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            image TEXT,
            category TEXT
        )
    ''')

    # 3. Замовлення (НОВЕ!)
    # Зв'язуємо замовлення з товаром через product_id
    c.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            customer_name TEXT NOT NULL,
            customer_phone TEXT NOT NULL,
            status TEXT DEFAULT 'New',
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# --- ВІДГУКИ ---
def add_feedback(name, email, message, rating):
    conn = get_db_connection()
    conn.execute('INSERT INTO feedback (name, email, message, rating) VALUES (?, ?, ?, ?)',
                 (name, email, message, rating))
    conn.commit()
    conn.close()

def get_all_feedback():
    conn = get_db_connection()
    reviews = conn.execute('SELECT * FROM feedback ORDER BY id DESC').fetchall()
    conn.close()
    return reviews

def delete_feedback(feedback_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM feedback WHERE id = ?', (feedback_id,))
    conn.commit()
    conn.close()

# --- ТОВАРИ ---
def add_product(name, price, image, category):
    conn = get_db_connection()
    conn.execute('INSERT INTO products (name, price, image, category) VALUES (?, ?, ?, ?)',
                 (name, price, image, category))
    conn.commit()
    conn.close()

def get_all_products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return products

def get_product_by_id(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()
    return product

def delete_product(product_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()

# --- ЗАМОВЛЕННЯ (НОВЕ) ---
def create_order(product_id, name, phone):
    conn = get_db_connection()
    conn.execute('INSERT INTO orders (product_id, customer_name, customer_phone) VALUES (?, ?, ?)',
                 (product_id, name, phone))
    conn.commit()
    conn.close()

def get_all_orders():
    conn = get_db_connection()
    # Об'єднуємо таблиці, щоб бачити назву товару, а не просто ID
    query = '''
        SELECT orders.id, orders.customer_name, orders.customer_phone, orders.status, products.name as product_name, products.price
        FROM orders
        JOIN products ON orders.product_id = products.id
        ORDER BY orders.id DESC
    '''
    orders = conn.execute(query).fetchall()
    conn.close()
    return orders

# --- ФУНКЦІЯ ДЛЯ ОНОВЛЕННЯ СТАТУСУ ---
def update_order_status(order_id, new_status):
    conn = get_db_connection()
    conn.execute('UPDATE orders SET status = ? WHERE id = ?', (new_status, order_id))
    conn.commit()
    conn.close()