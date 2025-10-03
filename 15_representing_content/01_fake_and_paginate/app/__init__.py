# -*- coding: utf-8 -*-

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import config


db = SQLAlchemy()
migrate = Migrate()

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    migrate.init_app(app, db=db)
    login_manager.init_app(app)

    from app.main.routes import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from app.auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    from app.utils import utils as utils_blueprint

    app.register_blueprint(utils_blueprint)

    from flask.cli import with_appcontext
    import click

    @app.cli.command("fill_db")
    @with_appcontext
    def fill_db():
        """Fill the database with fake users, todolists, and todos."""
        from utils.fake_generator import generate_all  # import diferido
        generate_all()
        click.echo("Database filled with fake data!")


    return app
