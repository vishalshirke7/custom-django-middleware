import unittest

from customapp.models import User, Token


class UserModelTest(unittest.TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='xyz', password='123')
        self.user2 = User.objects.create(username='xyz', password='123')

    def test_equal(self):
        self.assertEqual(self.user1.id, self.user2.id)

    def tearDown(self):
        del self.user1
        del self.user2
