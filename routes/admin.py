from flask import Blueprint, render_template, redirect, url_for, request
from models import get_all_feedback, delete_feedback

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
def admin_panel():
    reviews = get_all_feedback()
    return render_template('admin.html', title="Адмін-панель", reviews=reviews)

@admin_bp.route('/admin/delete_feedback/<int:id>')
def delete_review(id):
    delete_feedback(id)
    return redirect(url_for('admin.admin_panel'))