import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData

# Set naming convention for db constraints
# This enables SQLAlchemy migration autogeneration
# https://alembic.sqlalchemy.org/en/latest/naming.html
metadata = MetaData(naming_convention={
    'pk': 'pk_%(table_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'ix': 'ix_%(table_name)s_%(column_0_name)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
})
db = SQLAlchemy(metadata=metadata)


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
    migrate = Migrate(app, db)

    # Blueprints
    from . import index
    app.register_blueprint(index.bp)

    return app
