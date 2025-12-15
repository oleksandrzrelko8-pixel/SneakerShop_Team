from flask import Blueprint, render_template, request, redirect, url_for
from models import get_all_products, get_product_by_id, create_order

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html', title="Головна")

@main.route('/catalog')
def catalog():
    products = get_all_products()
    return render_template('catalog.html', title="Каталог", products=products)

# Сторінка оформлення замовлення (НОВЕ)
@main.route('/buy/<int:product_id>', methods=['GET', 'POST'])
def buy(product_id):
    # Знаходимо товар, який купують
    product = get_product_by_id(product_id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        
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