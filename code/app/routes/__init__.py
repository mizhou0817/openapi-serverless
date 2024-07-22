# from flask import Blueprint
#
# bp = Blueprint('routes', __name__)
#
# from .user_routes import bp as user_bp
# bp.register_blueprint(user_bp, url_prefix='/')

# from .account_routes import bp as account_bp


import os
import importlib
from flask_openapi3 import APIBlueprint

def register_blueprints(app):
    routes_dir = os.path.dirname(__file__)
    for filename in os.listdir(routes_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = f'app.routes.{filename[:-3]}'
            module = importlib.import_module(module_name)
            for attr in dir(module):
                attribute = getattr(module, attr)
                if isinstance(attribute, APIBlueprint):
                    app.register_api(attribute)