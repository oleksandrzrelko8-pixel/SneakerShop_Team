import sqlite3

def get_db_connection():
    conn = sqlite3.connect('db.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Створюємо таблицю для відгуків
    c.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            rating INTEGER DEFAULT 5
        )
    ''')
    
    # Створюємо таблицю для товарів (знадобиться пізніше)
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            image TEXT,
            category TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# --- Функції для роботи з відгуками ---

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