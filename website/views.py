from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify,request
from flask_login import login_required, current_user
from .models import Post, User,Comment,Like
from . import db
import requests
import json

views = Blueprint("views", __name__)

######################
## func=            ##
## home page        ##
######################


@views.route("/")
@views.route("/home",methods=["GET"])

@login_required
def home():
    req = requests.get('http://quotes.stormconsultancy.co.uk/random.json')
    # data=req.content
    data = json.loads(req.content)
    # print(req.content)
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts,data=data)

######################
## func=            ##
## delete a post    ##
######################

@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category='error')
    # elif current_user.id == post.id:
    #     flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')

    return redirect(url_for('views.home'))


######################
## func=            ##
## create a post    ##
######################


@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash('Post cannot be empty', category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('create_post.html', user=current_user)


######################
## func=            ##
## display a post   ##
######################


@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    posts = user.posts
    return render_template("posts.html", user=current_user, posts=posts, username=username)

######################### END
## func=                ##
## create a new comment ##
#########################

@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')

    return redirect(url_for('views.home'))

######################
## func=            ##
## delete a comment ##
######################

@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.home'))



    

