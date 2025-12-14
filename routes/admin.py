from flask import Blueprint, render_template, redirect, url_for, request
from models import get_all_feedback, delete_feedback, add_product, get_all_products

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    # Якщо адмін додає новий товар
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        image = request.form['image']
        category = request.form['category']
        
        add_product(name, price, image, category)
        return redirect(url_for('admin.admin_panel'))

    # Показуємо і відгуки, і товари
    reviews = get_all_feedback()
    products = get_all_products()
    return render_template('admin.html', title="Адмін-панель", reviews=reviews, products=products)

@admin_bp.route('/admin/delete_feedback/<int:id>')
def delete_review(id):
    delete_feedback(id)
    return redirect(url_for('admin.admin_panel'))