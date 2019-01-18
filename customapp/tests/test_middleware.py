import unittest

from django.test import RequestFactory

from customapp.middleware import AuthMiddleware


class AuthMiddlewateTest(unittest.TestCase):

    def setUp(self):
        self.middleware = AuthMiddleware()
        self.factory = RequestFactory()

    def test_requestProcessing(self):
        """
        This test case checks for authentication token in every request
        and if it is not present it tells to obtain one
        """

        request = self.factory.get('/test_api/')
        response = self.middleware.process_request(request)
        self.assertIsNotNone(response)

    def test_exempt_login(self):

        """
        This test case exempts login view from token authentication
        """
        request = self.factory.get('/api/v1/login')
        response = self.middleware.process_request(request)
        self.assertIsNone(response)
