import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('COVID_FUTURES_DATABASE_URI_TEST')
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('COVID_FUTURES_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Database
    db.init_app(app)

    # Blueprints
    from . import index
    app.register_blueprint(index.bp)

    return app
