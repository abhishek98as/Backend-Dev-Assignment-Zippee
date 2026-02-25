from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterTestCase(APITestCase):

    def test_register_success(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        res = self.client.post(url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', res.data)
        self.assertEqual(res.data['user']['username'], 'testuser')

    def test_register_missing_password(self):
        url = reverse('register')
        data = {'username': 'testuser2'}
        res = self.client.post(url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_username(self):
        User.objects.create_user(username='existinguser', password='pass123')
        url = reverse('register')
        data = {'username': 'existinguser', 'password': 'newpass123'}
        res = self.client.post(url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='loginuser', password='testpass123')

    def test_login_success(self):
        url = reverse('login')
        data = {'username': 'loginuser', 'password': 'testpass123'}
        res = self.client.post(url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)

    def test_login_invalid_password(self):
        url = reverse('login')
        data = {'username': 'loginuser', 'password': 'wrongpassword'}
        res = self.client.post(url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_nonexistent_user(self):
        url = reverse('login')
        data = {'username': 'nobody', 'password': 'somepass'}
        res = self.client.post(url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
