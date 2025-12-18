from flask import Blueprint, render_template, request, redirect, url_for
from models import get_all_products, get_product_by_id, create_order

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html', title="Головна")

@main.route('/catalog')
def catalog():
    # Підтримка пошуку та фільтрації
    q = request.args.get('q', '').lower()
    category = request.args.get('category', '')
    products = get_all_products()

    if q:
        products = [p for p in products if q in p['name'].lower() or q in (p.get('category') or '').lower()]
    if category:
        products = [p for p in products if (p.get('category') or '').lower() == category.lower()]

    return render_template('catalog.html', title="Каталог", products=products)

# Сторінка оформлення замовлення (НОВЕ)
@main.route('/buy/<int:product_id>', methods=['GET', 'POST'])
def buy(product_id):
    # Знаходимо товар, який купують
    product = get_product_by_id(product_id)
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()

        # basic validation
        if not name:
            from flask import flash
            flash('Ім\'я не може бути порожнім', 'danger')
            return render_template('order.html', title="Оформлення", product=product)
        if not phone or len(phone) < 7:
            from flask import flash
            flash('Вкажіть коректний телефон', 'danger')
            return render_template('order.html', title="Оформлення", product=product)

        # Створюємо замовлення
        create_order(product_id, name, phone)
        
        # Перенаправляємо на сторінку подяки
        return render_template('success.html', title="Дякуємо!")

    return render_template('order.html', title="Оформлення", product=product)

@main.route('/about')
def about():
    return render_template('about.html', title="Про нас")

@main.route('/contacts')
def contacts():
    return render_template('contacts.html', title="Контакти")