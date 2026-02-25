from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Task

User = get_user_model()


def get_token(user):
    """helper to get jwt token for a user"""
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


class TaskListTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='taskuser', password='pass123', role='user')
        self.token = get_token(self.user)
        # create some tasks
        Task.objects.create(title='Task 1', user=self.user)
        Task.objects.create(title='Task 2', user=self.user, completed=True)

    def test_list_tasks_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        res = self.client.get('/api/tasks/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 2)

    def test_list_tasks_unauthenticated(self):
        # unauthenticated users can still list tasks
        res = self.client.get('/api/tasks/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_filter_by_completed(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        res = self.client.get('/api/tasks/?completed=true')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 1)


class TaskCreateTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='creator', password='pass123', role='user')
        self.token = get_token(self.user)

    def test_create_task_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        data = {'title': 'My new task', 'description': 'some desc'}
        res = self.client.post('/api/tasks/', data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['title'], 'My new task')

    def test_create_task_unauthenticated(self):
        data = {'title': 'Should fail'}
        res = self.client.post('/api/tasks/', data, format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class TaskUpdateDeleteTestCase(APITestCase):

    def setUp(self):
        self.owner = User.objects.create_user(username='owner', password='pass123', role='user')
        self.other = User.objects.create_user(username='other', password='pass123', role='user')
        self.admin = User.objects.create_user(username='adminuser', password='pass123', role='admin')
        self.task = Task.objects.create(title='Owner task', user=self.owner)
        self.owner_token = get_token(self.owner)
        self.other_token = get_token(self.other)
        self.admin_token = get_token(self.admin)

    def test_owner_can_update_task(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.owner_token)
        res = self.client.patch(f'/api/tasks/{self.task.id}/', {'title': 'Updated'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], 'Updated')

    def test_other_user_cannot_update_task(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.other_token)
        res = self.client.patch(f'/api/tasks/{self.task.id}/', {'title': 'Hacked'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_update_any_task(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        res = self.client.patch(f'/api/tasks/{self.task.id}/', {'title': 'Admin edit'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_owner_can_delete_task(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.owner_token)
        res = self.client.delete(f'/api/tasks/{self.task.id}/')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_other_user_cannot_delete_task(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.other_token)
        res = self.client.delete(f'/api/tasks/{self.task.id}/')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
