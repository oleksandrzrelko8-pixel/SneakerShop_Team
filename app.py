from flask import Flask
from models import init_db
# Імпортуємо наші нові маршрути
from routes.main import main
from routes.feedback import feedback_bp
from routes.admin import admin_bp

app = Flask(__name__)

# Ініціалізуємо БД при запуску
with app.app_context():
    init_db()

# Реєструємо маршрути (Blueprints)
app.register_blueprint(main)
app.register_blueprint(feedback_bp)
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    app.run(debug=True)