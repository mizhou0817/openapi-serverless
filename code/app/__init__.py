from flask_openapi3 import OpenAPI, Info
from .utils.config import Config
from .routes import register_blueprints
from .utils.extensions import db


def create_app(config_class=Config):
    info = Info(title='Interview Manage API', version='1.0.0')
    app = OpenAPI(__name__, info=info)
    app.config.from_object(config_class)
    db.init_app(app)
    with app.app_context():
        register_blueprints(app)
    return app

app = create_app()