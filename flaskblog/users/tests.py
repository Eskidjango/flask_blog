from flask import Flask, url_for
from flaskblog import create_app
from flask_testing import TestCase


class UsersTestCases(TestCase):

    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    # def setUp(self):
    #     db.create_all()
    #
    # def tearDown(self):
    #     db.session.remove()
    #     db.drop_all()

    # def test_register_page_get(self):
    #     tester = app.test_client(self)
    #     response = tester.get('/register', follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)

    def test_register_page_invalid_form(self):
        tester = self.create_app().test_client(self)
        response = tester.post(
            url_for('users.register'),
            data={
                'email': 'test@test.com',
                'password': 'test',
                'confirm_password': 'test',
                'submit': True},
            follow_redirects=True
        )
        assert b'This field is required.' in response.data
        self.assert_template_used('register.html')
        self.assert200(response)