from flask import Flask, render_template, request, redirect, url_for, session, flash
from decorators import login_required
from extensions import db
from auth import auth
from posts import posts_bp
from users import users_bp
from main import main
from dotenv import load_dotenv
import os
from errors import errors


load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

    db.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(posts_bp)
    app.register_blueprint(users_bp)

    return app

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)