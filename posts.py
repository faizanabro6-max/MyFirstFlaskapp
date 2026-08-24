from flask import Blueprint, render_template, request, redirect, url_for,session,flash
from models import Post,User
from extensions import db
from decorators import login_required
from sqlalchemy.exc import SQLAlchemyError


posts_bp = Blueprint("posts", __name__)

@posts_bp.route("/posts")
def posts():
    posts = Post.query.all()
    return render_template("posts.html", posts=posts)

@posts_bp.route("/add-post", methods=["GET", "POST"])
@login_required
def add_post():

    if request.method == "POST":

        title = request.form["title"].strip()
        content = request.form["content"].strip()

        username = session.get("username")

        user = User.query.filter_by(username=username).first()

        if not title or not content:
         flash("Please fill in all fields", "error")
         return redirect(url_for("posts.add_post"))
        
        if len(title) < 3:
            flash("Title must contain atleast 3 Characters", "error")
            return redirect(url_for("posts.add_post"))

        if not user:
            return "User not found"

        post = Post(
            title=title,
            content=content,
            user_id=user.id
        )
        try:
            db.session.add(post)
            db.session.commit()

        except SQLAlchemyError:
            db.session.rollback()
            flash("Transaction failed", "error")
            return redirect(url_for("posts.add_post"))


        return redirect(url_for("posts.posts"))

    return render_template("add_post.html")

@posts_bp.route("/edit-post/<int:id>", methods=["GET", "POST"])
@login_required
def edit_post(id):

    post = db.get_or_404(Post, id)

    user_id = session.get("user_id")
    if post.user_id != user_id:
        print("NOT OWNER")
        return "You are not allowed to edit this post", 403

    if request.method == "POST":
        print("POST REQUEST")

        title = request.form["title"].strip()
        content = request.form["content"].strip()

        if not title or not content:
            flash("Please fill in all fields", "error")
            return redirect(url_for("posts.edit_post", id=id))

        if len(title) < 3:
            flash("Title must contain at least 3 characters", "error")
            return redirect(url_for("posts.edit_post", id=id))

        try:
            post.title = title
            post.content = content
            db.session.commit()

        except SQLAlchemyError:
            db.session.rollback()
            flash("Transaction failed", "error")
            return redirect(url_for("posts.edit_post", id=id))

        return redirect(url_for("posts.posts"))

    return render_template("edit_post.html", post=post)

@posts_bp.route("/delete-post/<int:id>", methods=["POST"])
@login_required
def delete_post(id):

    post = db.get_or_404(Post, id)

    user_id = session.get("user_id")

    if post.user_id != user_id:
     return "You are not allowed to delete this post", 403

    try:
     db.session.delete(post)
     db.session.commit()

    except SQLAlchemyError:
     db.session.rollback()
     flash("Transaction failed", "error")
     return redirect(url_for("posts.posts"))
    flash("Post deleted Successfully","success")

    return redirect(url_for("posts.posts"))