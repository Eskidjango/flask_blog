from dotenv import load_dotenv
load_dotenv()

from flask import url_for
from flask_testing import TestCase
from faker import Faker

from flaskblog import create_test_app, db, bcrypt
from flaskblog.models import User, Post


class UsersTestCases(TestCase):

    TESTING = True

    TEST_USERNAME = 'test'
    TEST_USER_EMAIL = 'test@test.com'
    TEST_PASSWORD = 'test'

    def create_app(self):
        app = create_test_app()
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        db.session.remove()
        db.drop_all()
        db.create_all()
        user = self.create_test_user()
        self.create_test_posts(user)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_test_user(self):
        hashed_password = bcrypt.generate_password_hash(self.TEST_PASSWORD).decode('utf-8')
        user = User(
            username=self.TEST_USERNAME,
            email=self.TEST_USER_EMAIL,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        return user

    def create_test_posts(self, user):
        fake = Faker()
        for _ in range(10):
            post = Post(
                title=fake.name(),
                content=fake.text(),
                user_id=user.id)
            db.session.add(post)
            db.session.commit()

    def login(self, client, email=None, password=None):
        email = email or self.TEST_USER_EMAIL
        password = password or self.TEST_PASSWORD
        return client.post(
            url_for('users.login'),
            data={
                'email': email,
                'password': password,
                'submit': True
                },
            follow_redirects=True
        )

    def logout(self, client):
        return client.get(url_for('users.logout'), follow_redirects=True)

    # Testing user's routes
    def test_register_page_get(self):
        """
        check if register page shows up correctly

        :return:
        """
        tester = self.create_app().test_client(self)
        response = tester.get(url_for('users.register'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_register_page_invalid_form(self):
        """
        check if invalid form processing works correctly

        :return:
        """
        tester = self.create_app().test_client(self)
        response = tester.post(
            url_for('users.register'),
            # Not included 'username' field
            data={
                'email': 'some_test_user@test.com',
                'password': 'some_test_password',
                'confirm_password': 'some_test_password',
                'submit': True},
            follow_redirects=True
        )
        assert b'Your account has been created! You are now able to log in' not in response.data
        assert b'This field is required.' in response.data
        self.assert_template_used('register.html')
        self.assert200(response)

    def test_register_page_valid_form(self):
        """
        check if valid form processing works correctly

        :return:
        """
        tester = self.create_app().test_client(self)
        response = tester.post(
            url_for('users.register'),
            data={
                'username': 'test1',
                'email': 'test1@test.com',
                'password': 'test1',
                'confirm_password': 'test1',
                'submit': True},
            follow_redirects=True
        )
        assert b'Your account has been created! You are now able to log in' in response.data
        self.assert_template_used('login.html')
        self.assert200(response)

    def test_login_page_get(self):
        """
        check if register page shows up correctly

        :return:
        """
        tester = self.create_app().test_client(self)
        response = tester.get(url_for('users.login'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_page_invalid_form(self):
        """
        check if invalid form processing works correctly

        :return:
        """
        tester = self.create_app().test_client(self)
        response = self.login(tester, email='zozochka@mail.kozochka')
        assert b'Login Unsuccessful. Please check email and password' in response.data
        self.assert_template_used('login.html')
        self.assert200(response)
        response = self.login(tester)
        self.assert_template_used('home.html')
        self.assert200(response)

    def test_login_page_valid_form(self):
        """
        check if invalid form processing works correctly

        :return:
        """
        tester = self.create_app().test_client(self)
        response = self.login(tester)
        self.assert_template_used('home.html')
        self.assert200(response)

    def test_logout_get(self):
        tester = self.create_app().test_client(self)
        response = self.logout(tester)
        self.assert200(response)

    def test_account_page_get(self):
        """
        check if register page shows up correctly

        :return:
        """
        tester = self.create_app().test_client(self)
        response = tester.get(url_for('users.account'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    #
    def test_account_page_invalid_form(self):
        """
        check if invalid form processing works correctly

        :return:
        """
        tester = self.create_app().test_client(self)
        self.login(tester)
        response = tester.post(
            url_for('users.account'),
            data={
                'email': self.TEST_USER_EMAIL,
                'picture': 'test_jpeg.jpg',
                'submit': True
            },
            follow_redirects=True)
        assert self.TEST_USERNAME.encode() in response.data
        assert self.TEST_USER_EMAIL.encode() in response.data
        self.assert_template_used('account.html')
        self.assert200(response)

    def test_account_page_valid_form(self):
        """
        check if invalid form processing works correctly

        :return:
        """
        tester = self.create_app().test_client(self)
        self.login(tester)
        response = tester.post(
            url_for('users.account'),
            data={
            'username': 'vasek_pitek',
            'email': 'vasichka@kozochka.com',
            'picture': 'test_jpeg.jpg',
            'submit': True
        },
            follow_redirects=True)
        self.assert_template_used('account.html')
        self.assert200(response)

    def test_user_posts(self):
        tester = self.create_app().test_client(self)
        response = tester.get(
            url_for('users.user_posts', username='test'),
            data={'page': 1},
            follow_redirects=True)