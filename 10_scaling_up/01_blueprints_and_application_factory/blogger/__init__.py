from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'hello_world'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Import and register blueprints
    from .auth import auth
    from .blog import blog
    from .main import main

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(blog, url_prefix='/blog')
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app

