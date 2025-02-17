import unittest
import json
import time

from project.server import db
from project.server.models import User, BlacklistToken
from project.tests.base_test import BaseTestCase


class TestAuthBlueprint(BaseTestCase):
    def test_registration(self):
        with self.client:
            response = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    email='monty@gmail.com',
                    password='123456',
                    first_name='monty',
                    last_name='python',
                    is_admin='0'
                )), content_type='application/json'
            )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully registered.')
        self.assertTrue(data['auth_token'])
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 201)

    def test_registered_with_already_registered_user(self):
        user = User(
            email='monty@gmail.com',
            password='123456',
            first_name='monty',
            last_name='python',
            is_admin='0'
        )

        db.session.add(user)
        db.session.commit()
        with self.client:
            response = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    email='monty@gmail.com',
                    password='123456',
                    first_name='monty',
                    last_name='python',
                    is_admin=0
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'User already exists. Please Log in.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 202)

    def test_registered_user_login(self):
        with self.client:
            resp_register = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    email='monty@gmail.com',
                    password='123456',
                    first_name='monty',
                    last_name='python',
                    is_admin='0'
                )),
                content_type='application/json',
            )
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(
                data_register['message'] == 'Successfully registered.'
            )
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            response = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    email='monty@gmail.com',
                    password='123456'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_non_registered_user_login(self):
        with self.client:
            response = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    email='nomonty@gmail.com',
                    password='123456'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'User does not exist.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 404)

    def test_user_status(self):
        with self.client:
            resp_register = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    email='monty@gmail.com',
                    password='123456',
                    first_name='monty',
                    last_name='python',
                    is_admin='0'
                )),
                content_type='application/json'
            )
            response = self.client.get(
                '/api/v1/auth/status',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['data'] is not None)
            self.assertTrue(data['data']['email'] == 'monty@gmail.com')
            self.assertEqual(response.status_code, 200)

    def test_valid_logout(self):
        with self.client:
            resp_register = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    email='monty@gmail.com',
                    password='123456',
                    first_name='monty',
                    last_name='python',
                    is_admin='0'
                )),
                content_type='application/json',
            )
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(
                data_register['message'] == 'Successfully registered.')
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            resp_login = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    email='monty@gmail.com',
                    password='123456'
                )),
                content_type='application/json'
            )
            data_login = json.loads(resp_login.data.decode())
            self.assertTrue(data_login['status'] == 'success')
            self.assertTrue(data_login['message'] == 'Successfully logged in.')
            self.assertTrue(data_login['auth_token'])
            self.assertTrue(resp_login.content_type == 'application/json')
            self.assertEqual(resp_login.status_code, 200)
            response = self.client.post(
                '/api/v1/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged out.')
            self.assertEqual(response.status_code, 200)

    def test_valid_blacklisted_token_logout(self):
        with self.client:
            resp_register = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    email='monty@gmail.com',
                    password='123456',
                    first_name='monty',
                    last_name='python',
                    is_admin='0'
                )),
                content_type='application/json',
            )
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(
                data_register['message'] == 'Successfully registered.')
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            resp_login = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    email='monty@gmail.com',
                    password='123456'
                )),
                content_type='application/json'
            )
            data_login = json.loads(resp_login.data.decode())
            self.assertTrue(data_login['status'] == 'success')
            self.assertTrue(data_login['message'] == 'Successfully logged in.')
            self.assertTrue(data_login['auth_token'])
            self.assertTrue(resp_login.content_type == 'application/json')
            self.assertEqual(resp_login.status_code, 200)
            blacklist_token = BlacklistToken(
                token=json.loads(resp_login.data.decode())['auth_token'])
            db.session.add(blacklist_token)
            db.session.commit()
            response = self.client.post(
                '/api/v1/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Token blacklisted. Please log in again.')
            self.assertEqual(response.status_code, 401)

    def test_decode_auth_token(self):
        user = User(
            email='monty@gmail.com',
            password='123456',
            first_name='monty',
            last_name='python',
            is_admin='0'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id, user.is_admin)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(
            auth_token.decode("utf-8")) == 1)


if __name__ == '__main__':
    unittest.main()
