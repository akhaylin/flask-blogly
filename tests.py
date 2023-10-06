import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"

from unittest import TestCase

from app import app, db
from models import User, Post

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()


        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        db.session.add(test_user)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        """Tests to see if users are displayed on page"""

        with app.test_client() as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_show_user(self):
        """Test if user profile displays the users information"""

        with app.test_client() as c:
            resp = c.get(f"/users/{self.user_id}", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_add_user(self):
        """Test to see if user gets added to db and is displayed on page"""

        with app.test_client() as c:
            data = {"first_name": "Joe", "last_name": "Musk", "image_url": "jpeg"}
            resp = c.post('/users/new',data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertIn("Joe", html)
            self.assertIn("Musk", html)

    def test_delete_user(self):
        """Test to see if user gets deleted from db and does not appear on users
            page
        """

        with app.test_client() as c:
            resp = c.post(f"/users/1/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertNotIn("test1_first", html)
            self.assertNotIn("test1_last", html)



class PostTestCase(TestCase):
    """Test views for posts."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()


        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        db.session.add(test_user)
        db.session.commit()

        test_post = Post(
            title='test_post_title',
            content='testing_testing_testing_content',
            user_id=test_user.id
        )

        db.session.add(test_post)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id
        self.post_id= test_post.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()


    def test_show_post_on_user(self):
        """Test if post shows up on user profile page"""
        with app.test_client() as c:
            resp = c.get(f'/users/{self.user_id}')
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test_post_title", html)

    ##TODO:Change to test follow redirect and then check if new post is on page
    def test_add_post_redirect(self):
        """Test adding post redirect to user profile page"""

        with app.test_client() as c:
            data = {"title": "User Post", "content": "GOOD MORNING", "user_id": self.user_id}
            resp = c.post(f'/users/{self.user_id}/posts/new', data=data)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 302)

    ##TODO:Check for content too
    def test_show_post_details(self):
        """Test the show post details"""

        with app.test_client() as c:
            resp = c.get(f'/posts/{self.post_id}')
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test_post_title", html)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    ##TODO:Check if content is in form
    def test_show_post_edit_form(self):
        """Test to check if post edit form is rendered"""

        with app.test_client() as c:
            resp = c.get(f'/posts/{self.post_id}/edit')
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("Edit Post", html)

    def test_edit_post(self):
        """Test editing a post check if title has changed on redirect"""

        with app.test_client() as c:
            data={"title": "This Title Changed", "content": "testing_testing_testing_content"}
            resp = c.post(f'/posts/{self.post_id}/edit', data=data, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("This Title Changed", html)

    ##TODO:Put in user class
    def test_delete_user_having_posts(self):
        """Test to see if user gets deleted from db while they have posts written
            by them
        """

        with app.test_client() as c:
            resp = c.post(f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertNotIn("test1_first", html)
            self.assertNotIn("test1_last", html)

    def test_delete_post(self):
        """Test deleting a post from the db"""

        with app.test_client() as c:
            resp = c.post(f"/posts/{self.post_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("test_post_title", html)






