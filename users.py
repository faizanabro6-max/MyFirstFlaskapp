from flask import Blueprint, render_template, request, redirect, url_for
from models import User
from extensions import db

users_bp = Blueprint("users", __name__)

@users_bp.route("/users")
def users():
    users = User.query.all()
    return render_template("users.html", users=users)

@users_bp.route("/delete-user/<int:id>")
def delete_user(id):

    user = db.session.get(User, id)

    if user:
        db.session.delete(user)
        db.session.commit()

    return redirect(url_for("users.users"))


@users_bp.route("/find-user")
def find_user():

    user = db.session.get(User, 2)

    if user:
        return f"Found: {user.username} - {user.email}"

    return "User not found"

@users_bp.route("/user/<int:id>")
def user_profile(id):

    user = db.session.get(User, id)

    if not user:
        return "User not found"

    return render_template("user_profile.html", user=user)





