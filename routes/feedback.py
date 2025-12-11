from flask import Blueprint, render_template, request, redirect, url_for
from models import add_feedback, get_all_feedback

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        rating = request.form.get('rating', 5) # За замовчуванням 5
        
        add_feedback(name, email, message, rating)
        return redirect(url_for('feedback.feedback'))
    
    # Отримуємо всі відгуки, щоб показати їх на сторінці
    reviews = get_all_feedback()
    return render_template('feedback.html', title="Відгуки", reviews=reviews)