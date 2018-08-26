import os
from dotenv import load_dotenv

from flaskblog.models import User

load_dotenv()

from flask import Flask, url_for
from flaskblog import create_test_app, db, bcrypt
from flask_login import login_user, logout_user
from flask_testing import TestCase


class UsersTestCases(TestCase):

    TESTING = True

    def create_app(self):
        app = create_test_app()
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        db.create_all()
        self.user = self.create_test_user()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_test_user(self):
        hashed_password = bcrypt.generate_password_hash('test').decode('utf-8')
        user = User(
            username='test',
            email='test@test.com',
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        return user

    def login(self, client, email, password):
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

    # # Testing user's routes
    # def test_register_page_get(self):
    #     """
    #     check if register page shows up correctly
    #
    #     :return:
    #     """
    #     tester = self.create_app().test_client(self)
    #     response = tester.get(url_for('users.register'), follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_register_page_invalid_form(self):
    #     """
    #     check if invalid form processing works correctly
    #
    #     :return:
    #     """
    #     tester = self.create_app().test_client(self)
    #     response = tester.post(
    #         url_for('users.register'),
    #         # Not included 'username' field
    #         data={
    #             'email': 'some_test_user@test.com',
    #             'password': 'some_test_password',
    #             'confirm_password': 'some_test_password',
    #             'submit': True},
    #         follow_redirects=True
    #     )
    #     assert b'Your account has been created! You are now able to log in' not in response.data
    #     assert b'This field is required.' in response.data
    #     self.assert_template_used('register.html')
    #     self.assert200(response)
    #
    # def test_register_page_valid_form(self):
    #     """
    #     check if valid form processing works correctly
    #
    #     :return:
    #     """
    #     tester = self.create_app().test_client(self)
    #     response = tester.post(
    #         url_for('users.register'),
    #         data={
    #             'username': 'test',
    #             'email': 'test@test.com',
    #             'password': 'test',
    #             'confirm_password': 'test',
    #             'submit': True},
    #         follow_redirects=True
    #     )
    #     assert b'Your account has been created! You are now able to log in' in response.data
    #     self.assert_template_used('login.html')
    #     self.assert200(response)

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
        """
                check if invalid form processing works correctly

                :return:
                """
        tester = self.create_app().test_client(self)
        response = self.login(tester, 'test@test.com', 'zozochka')
        assert b'Login Unsuccessful. Please check email and password' in response.data
        self.assert_template_used('login.html')
        self.assert200(response)

    def test_login_page_valid_form(self):
        """
        check if invalid form processing works correctly

        :return:
        """
        tester = self.create_app().test_client(self)
        response = self.login(tester, 'test@test.com', 'test')
        self.assert_template_used('home.html')
        self.assert200(response)