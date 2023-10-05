"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


@app.get('/')
def home():
    """"Redirects to users page show list of users"""

    return redirect('/users')


@app.get('/users')
def list_users():
    """Gets all users from databse and displays as list"""
    ##TODO:Order by last/first name method order_by

    users = User.query.all()
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
    ##TODO:Flash message indicating succcess/fail
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

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
    ##TODO:Flash message for updated info success
    user = User.query.get_or_404(user_id)

    if request.form["first_name"]:
        user.first_name = request.form["first_name"]
    if request.form["last_name"]:
        user.last_name = request.form["last_name"]
    if request.form["image_url"]:
        user.image_url = request.form["image_url"]

    db.session.commit()

    return redirect('/users')


@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Deletes a user from the database then returns to users page"""

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/users')




