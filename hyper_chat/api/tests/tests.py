from django.test import TestCase
# Create your tests here.
from ..models import Chatter
from rest_framework.test import APITestCase


class AuthedTestCase(APITestCase):
    def setUp(self):
        user = Chatter.objects.create(username='test1234', nickname='test1234')
        user.set_password('test1234')
        user.save()

        login_response = self.client.post('/api/auth', {'username': 'test1234', 'password': 'test1234'})

        self.assertEqual(login_response.status_code, 200)
        self.assertIn('token', login_response.data)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_response.data['token'])
        self.user_id = user.id


