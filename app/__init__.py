import os
from flask import Flask
from .models import db
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    load_dotenv() # Load environment variables from .env

    # --- Configuration ---
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    # Configure the SQLite database
    # The database file will be located in the 'instance' folder
    db_path = os.path.join(app.instance_path, 'app.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass # Already exists

    # --- Initialize Extensions ---
    db.init_app(app)

    with app.app_context():
        # Import routes and models here to avoid circular imports
        from . import routes
        db.create_all() # Create sql tables for our data models

    return app