from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from decorators import login_required

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("index.html")

@main.route("/about/<name>")
def about(name):
    students=["Faizan","sam","john"]
    return render_template(
        "about.html",name=name,
        course= "Flask Backend Development",
        students=students
    )

@main.route("/contact",methods=["GET","POST"])
def contact():
    if request.method =="POST":
        flash("Your Form is Successfully Submitted")
        return redirect(url_for("main.contact"))
    return render_template("contact.html")

@main.route("/method", methods=["GET", "POST"])
def method():
    return request.method

@main.route("/profile")
@login_required
def profile():
    username = session.get("username")
    return "Welcome " + username