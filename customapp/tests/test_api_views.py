import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from customapp.models import User, Token


class LoginTest(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='xyz', password='123')

    def test_login(self):
        """
        Checking whether token returned on login is associated with same user.
        """

        url = reverse('customapp:login')
        data = {'username': 'xyz', 'password': '123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        key = json.loads(response.content)
        token = Token.objects.get(key=key['token'])
        self.assertEqual(self.user1.id, token.user.id)

    def tearDown(self):
        del self.user1


class CheckAuthentication(APITestCase):

    client = APIClient()

    def setUp(self):
        url = reverse('customapp:login')
        data = {'username': 'xyz', 'password': '123'}
        response = self.client.post(url, data, format='json')
        data = json.loads(response.content)
        self.key = data['token']

    def test_api(self):
        """
        calling test api without token
        """

        url = reverse('customapp:testapi')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(json.loads(response.content), {'error': 'No authentication header provided'})

    def test_with_token(self):
        """
        Testing api with token in the authorization header
        """
        token = Token.objects.get(key=self.key)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = reverse('customapp:testapi')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

