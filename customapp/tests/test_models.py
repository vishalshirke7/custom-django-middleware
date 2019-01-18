import unittest

from customapp.models import User, Token


class UserModelTest(unittest.TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='xyz', password='123')
        self.user2 = User.objects.create(username='xyz', password='567')

    def test_equal(self):
        self.assertNotEqual(self.user1.id, self.user2.id)

    def tearDown(self):
        del self.user1
        del self.user2


class TokenModelTest(unittest.TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='xyz', password='123')
        self.token = Token.objects.create(user=self.user1)
        self.token1 = Token.objects.create(user=self.user1)

    def test_token(self):
        self.assertNotEqual(self.token, self.token1)

    def tearDown(self):
        del self.user1
        del self.token
        del self.token1