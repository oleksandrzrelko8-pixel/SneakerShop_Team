from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from models import init_db
from routes.main import main
from routes.feedback import feedback_bp
from routes.admin import admin_bp
from routes.api import api_bp

from extensions import csrf

app = Flask(__name__)
CORS(app)
csrf.init_app(app)

# Swagger configuration
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger = Swagger(app, config=swagger_config)

# Секретний ключ для сесій (міняти у production через змінні оточення)
import os
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')

with app.app_context():
    init_db()

app.register_blueprint(main)
app.register_blueprint(feedback_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(api_bp)

if __name__ == '__main__':
    # Створення таблиць (якщо треба)
    with app.app_context():
        pass

    # Для локальної розробки використовується FLASK_DEBUG, у production повинен запускатись Gunicorn
    debug_flag = os.environ.get('FLASK_DEBUG', 'False').lower() in ('1', 'true', 'yes')
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=debug_flag)