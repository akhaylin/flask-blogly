"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'super_secret'

connect_db(app)

@app.get('/')
def home():
    """"Redirects to users page show list of users"""

    return redirect('/users')


@app.get('/users')
def list_users():
    """Gets all users from databse and displays as list"""

    users = User.query.order_by(User.first_name).all()
    return render_template('users.html', users=users)


@app.get('/users/new')
def new_user_form():
    """Display form to create a new user"""

    return render_template('create_user.html')


@app.post('/users/new')
def add_new_user():
    """Handle create user form submisssion, creates user in database
       redirects to users page
    """

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    try:
        user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(user)
        db.session.commit()
        flash('User added successfully', 'success')
    except Exception:
        flash('Error while adding user', 'danger')

    return redirect('/users')


@app.get('/users/<int:user_id>')
def show_user(user_id):
    """"Display specific users profile page"""

    user = User.query.get_or_404(user_id)

    return render_template('user_detail.html', user=user)


@app.get('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Display the edit user info form"""

    user = User.query.get_or_404(user_id)

    return render_template('edit_user_page.html', user=user)


@app.post('/users/<int:user_id>/edit')
def update_user(user_id):
    """Handles edit profile form submission, edits user information in database
        redirects to users page after completing edit
    """

    user = User.query.get_or_404(user_id)

    if request.form["first_name"]:
        user.first_name = request.form["first_name"]
    if request.form["last_name"]:
        user.last_name = request.form["last_name"]
    if request.form["image_url"]:
        user.image_url = request.form["image_url"]

    db.session.commit()
    flash('Updated user successfully', 'success')

    return redirect('/users')


@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Deletes a user from the database then returns to users page"""

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


@app.get('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    """Shows the new post form when user clicks add post"""

    user = User.query.get_or_404(user_id)

    return render_template('new_post.html', user=user)


@app.post('/users/<int:user_id>/posts/new')
def add_post(user_id):
    title = request.form["title"]
    content = request.form["content"]

    post = Post(title=title, content=content, user_id=user_id )
    db.session.add(post)
    db.session.commit()
    flash("Post added successfully!", "success")

    return redirect(f"/users/{user_id}")


@app.get('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    user = post.user

    return render_template('post_detail.html', post=post, user=user)


@app.get('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)

    return render_template('post_edit.html', post=post)








