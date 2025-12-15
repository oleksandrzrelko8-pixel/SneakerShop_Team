from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from models import init_db
from routes.main import main
from routes.feedback import feedback_bp
from routes.admin import admin_bp
from routes.api import api_bp

app = Flask(__name__)
CORS(app)

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

with app.app_context():
    init_db()

app.register_blueprint(main)
app.register_blueprint(feedback_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(debug=True)