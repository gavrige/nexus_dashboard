import os
from flask import Flask
from .models import db
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    load_dotenv()

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    db_path = os.path.join(app.instance_path, 'app.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    with app.app_context():
        # Import and register the blueprint
        from . import routes
        app.register_blueprint(routes.bp)

        # Create database tables
        db.create_all()

    return app