from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from decorators import login_required
from models import Post
from extensions import db
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

@main.route("/api/hello")
def api_hello():
    return{
        "message":"Hello from FLask API",
        "Status":"Success"
    }

@main.route("/api/posts")
def api_posts():

    posts = Post.query.all()

    return { 
        "success":True,
        "message":"Posts retrived succesfully",
        "data":[
            {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "user_id": post.user_id
            }
            for post in posts
        ]
    }


@main.route("/api/posts/<int:id>")
def api_post(id):

    post = db.get_or_404(Post, id)

    return {
        "success": True,
        "message": "Post retrieved successfully",
        "data": {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "user_id": post.user_id
    }
}

@main.route("/api/posts", methods=["POST"])
@login_required
def create_api_post():

    data = request.get_json(silent=True)
    if data is None:
        return{
            "error":"JSON data is required"
        },400
    title = data.get("title")
    content = data.get("content")

    if not title or not content:
        return {
            "error": "Title and content are required"
        }, 400

    post = Post(
        title=title,
        content=content,
        user_id=session["user_id"]
    )
    db.session.add(post)
    db.session.commit()

    return {
        "success":True,
        "message":"Post created successfully",
        "data":{
            "post_id":post.id
        }
    }, 201

@main.route("/api/posts/<int:id>", methods=["PUT"])
def update_api_post(id):
    post = db.get_or_404(Post,id)
    data = request.get_json(silent=True)

    if data is None:
        return{
            "error":"JSON data is required"
        },400
    
    title = data.get("title")
    content= data.get("content")

    if not title or not content:
        return{
            "error":"Title and content are required"
        }, 400

    if post.user_id !=session["user_id"]:
        return{
            "success":False,
            "error":"You are not allowed to edit this post"
        },403

    post.title = title
    post.content = content

    db.session.commit()

    return{
        "success":True,
        "message":"Post updated successfully",
        "data":{
            "post_id":post.id

        }
    },200

@login_required
@main.route("/api/posts/<int:id>", methods=["DELETE"])
def delete_api_post(id):
    post = db.get_or_404(Post,id)

    if post.user_id !=session["user_id"]:
       return{
            "success":False,
            "error":"You are not allowed to delete this post"
    },403

    db.session.delete(post)
    db.session.commit()

    return{
        "success":True,
        "message":"Post is deleted successfully",
        "data":{
            "post_id":post.id
        }
    }
