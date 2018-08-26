import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, url_for
from flaskblog import create_test_app, db
from flask_testing import TestCase


class UsersTestCases(TestCase):

    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_TEST')
    # TESTING = True

    def create_app(self):
        app = create_test_app()
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Testing user's routes
    def test_register_page_get(self):
        """
        check if register page shows up correctly

        :return:
        """
        tester = self.create_app().test_client(self)
        response = tester.get('/register', follow_redirects=True)
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
                'email': 'test@test.com',
                'password': 'test',
                'confirm_password': 'test',
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
                'username': 'test',
                'email': 'test@test.com',
                'password': 'test',
                'confirm_password': 'test',
                'submit': True},
            follow_redirects=True
        )
        assert b'Your account has been created! You are now able to log in' in response.data
        self.assert_template_used('login.html')
        self.assert200(response)



