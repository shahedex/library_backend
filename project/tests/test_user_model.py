import unittest

from project.server import db
from project.server.models import User
from project.tests.base_test import BaseTestCase


class TestUserModel(BaseTestCase):

    def test_encode_auth_token(self):
        user = User(
            email='test@test.com',
            password='testPass',
            first_name='test',
            last_name='user',
            is_admin=0
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id, user.is_admin)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = User(
            email='test@test.com',
            password='testPass',
            first_name='test',
            last_name='user',
            is_admin=0
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id, user.is_admin)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token) == user.id)

if __name__ == '__main__':
    unittest.main()