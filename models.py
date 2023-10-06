from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)
"""Models for Blogly."""

class User(db.Model):
    """"Users class"""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    first_name = db.Column(
        db.String(20),
        nullable=False)

    last_name = db.Column(
        db.String(20),
        nullable=False)

    image_url = db.Column(
        db.Text
    )
    # posts = db.relationship('Post', backref='users') IF relationship was in this class it would look liek this

class Post(db.Model):
    """Posts class"""

    __tablename__ = "posts"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    title = db.Column(
        db.String(50),
        nullable=False)

    content = db.Column(
        db.Text,
        nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=db.func.now(),
        nullable=False
    )
##TODO:make foerign key not nullable
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )

    user = db.relationship('User', backref='posts')
