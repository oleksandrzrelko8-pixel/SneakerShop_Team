from flask import Blueprint, render_template
from models import get_all_products

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html', title="Головна")

@main.route('/catalog')
def catalog():
    # Тепер товари беруться з Бази Даних!
    products = get_all_products()
    return render_template('catalog.html', title="Каталог", products=products)

@main.route('/about')
def about():
    return render_template('about.html', title="Про нас")

@main.route('/contacts')
def contacts():
    return render_template('contacts.html', title="Контакти")