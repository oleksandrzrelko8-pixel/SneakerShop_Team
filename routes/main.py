from flask import Blueprint, render_template

# Оголошуємо Blueprint (це наче гілка маршрутів)
main = Blueprint('main', __name__)

# --- СЮДИ МИ ПЕРЕНЕСЛИ МАРШРУТИ З APP.PY ---

@main.route('/')
def home():
    return render_template('index.html', title="Головна")

@main.route('/catalog')
def catalog():
    # Пізніше ми тут підключимо базу даних, а поки лишаємо як було
    return render_template('catalog.html', title="Каталог")

@main.route('/about')
def about():
    return render_template('about.html', title="Про нас")

@main.route('/contacts')
def contacts():
    return render_template('contacts.html', title="Контакти")