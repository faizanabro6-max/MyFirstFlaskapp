from flask import Blueprint , request, redirect, url_for, render_template, flash, session
from models import User
from werkzeug.security import check_password_hash, generate_password_hash
from extensions import db
from sqlalchemy.exc import SQLAlchemyError

auth = Blueprint("auth", __name__)
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if not user:
            flash("User not found", "error")
            return redirect(url_for("auth.login"))

        if not check_password_hash(user.password, password):
            flash("Incorrect password", "error")
            return redirect(url_for("auth.login"))
        
        session["username"] = user.username
        session["user_id"] = user.id
        flash("Login successful!", "success")
        return redirect(url_for("main.profile"))
    return render_template("login.html")

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
     username = request.form["username"]
     email = request.form["email"]
     password = request.form["password"]
     confirm_password = request.form["confirm_password"]
     if password != confirm_password:
         flash("Password Doesn't Match", "error")
         return redirect(url_for("auth.register"))
    
     if not username or not email or not password:
        flash("Please fill in all feilds", "error")
        return redirect(url_for("auth.register"))
     
     existing_user = User.query.filter_by(username=username).first()
     if existing_user:
         flash("This username is already registered", "error")
         return redirect(url_for("auth.register"))
     
     existing_email = User.query.filter_by(email=email).first()
     if existing_email:
         flash("This email is already registered", "error")
         return redirect(url_for("auth.register"))
     
     password_hash = generate_password_hash(password)
     user = User(
     username=username,
     email=email,
     password=password_hash
     )
     
     try:
         db.session.add(user)
         db.session.commit()
        

     except SQLAlchemyError:
         db.session.rollback()
         flash("Transaction failed", "error")
         return redirect(url_for("auth.register"))    
     return redirect(url_for("auth.login"))

    return render_template("register.html")

@auth.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("user_id", None)
    return "You Logged Out!"

    
    

        
