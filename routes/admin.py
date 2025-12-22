from flask import Blueprint, render_template, redirect, url_for, request, session, flash
import os
from functools import wraps
from models import get_all_feedback, delete_feedback, add_product, get_all_products, get_all_orders, update_order_status, delete_product, update_product

# ІМПОРТУЄМО CSRF ДЛЯ ВИМКНЕННЯ ПЕРЕВІРКИ
from extensions import csrf

admin_bp = Blueprint('admin', __name__)

# Простий декоратор для захисту адмін-роутів
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('is_admin'):
            return redirect(url_for('admin.login', next=request.path))
        return f(*args, **kwargs)
    return decorated

@admin_bp.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password', '')
        if password == os.environ.get('ADMIN_PASSWORD', 'admin123'):
            session['is_admin'] = True
            flash('Вхід успішний', 'success')
            next_url = request.args.get('next') or url_for('admin.admin_panel')
            return redirect(next_url)
        else:
            flash('Невірний пароль', 'danger')
    return render_template('admin_login.html')

@admin_bp.route('/admin/logout')
def logout():
    session.pop('is_admin', None)
    flash('Ви вийшли з адмін-панелі', 'info')
    return redirect(url_for('main.index'))

@admin_bp.route('/admin', methods=['GET', 'POST'])
@admin_required
@csrf.exempt
def admin_panel():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        price_raw = request.form.get('price', '').strip()
        image = request.form.get('image', '').strip()
        category = request.form.get('category', 'General').strip()
        product_id = request.form.get('product_id', '').strip()

        if not name:
            flash('Назва товару не може бути порожньою', 'danger')
            return redirect(url_for('admin.admin_panel'))
        
        try:
            price = float(price_raw)
        except ValueError:
            flash('Ціна має бути числом', 'danger')
            return redirect(url_for('admin.admin_panel'))

        if product_id:
            try:
                update_product(int(product_id), name, price, image, category)
                flash('Товар оновлено', 'success')
            except Exception as e:
                flash(f'Помилка при оновленні: {e}', 'danger')
        else:
            try:
                add_product(str(name), float(price), str(image), str(category))
                flash('Товар додано успішно!', 'success')
            except Exception as e:
                flash(f'Помилка бази даних: {e}', 'danger')
        
        return redirect(url_for('admin.admin_panel'))

    reviews = get_all_feedback()
    products = get_all_products()
    orders = get_all_orders()
    return render_template('admin.html', title="Адмін-панель", reviews=reviews, products=products, orders=orders)

@admin_bp.route('/admin/delete_feedback/<int:id>')
@admin_required
def delete_review(id):
    delete_feedback(id)
    flash('Відгук видалено', 'info')
    return redirect(url_for('admin.admin_panel'))

@admin_bp.route('/admin/delete_product/<int:id>')
@admin_required
def delete_product_route(id):
    delete_product(id)
    flash('Товар видалено', 'info')
    return redirect(url_for('admin.admin_panel'))

@admin_bp.route('/admin/order/<int:id>/<string:status>')
@admin_required
def change_status(id, status):
    update_order_status(id, status)
    flash('Статус оновлено', 'success')
    return redirect(url_for('admin.admin_panel'))