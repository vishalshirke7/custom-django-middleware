import unittest

from django.test import RequestFactory

from customapp.middleware import AuthMiddleware


class AuthMiddlewateTest(unittest.TestCase):

    def setUp(self):
        self.middleware = AuthMiddleware()
        self.factory = RequestFactory()

    def test_requestProcessing(self):
        """
        Failure Test case. It checks for authentication token in every request

        """
        request = self.factory.get('/test_api/')
        response = self.middleware.process_request(request)
        self.assertIsNone(response)

    def test_exempt_login(self):

        """
        This test case exempts login view from token authentication
        """
        request = self.factory.get('/api/v1/login')
        response = self.middleware.process_request(request)
        self.assertIsNone(response)
