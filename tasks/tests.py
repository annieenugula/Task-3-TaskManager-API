from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Task


class AuthTestCase(APITestCase):

    def test_register_user(self):
        data = {
            'username': 'newuser',
            'password': 'Pass@1234',
            'email': 'new@test.com'
        }
        response = self.client.post(
            '/api/auth/register/',
            data,
            format='json'
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['username'], 'newuser')

    def test_login_valid(self):
        User.objects.create_user(
            'loginuser',
            password='Pass@1234'
        )

        data = {
            'username': 'loginuser',
            'password': 'Pass@1234'
        }

        response = self.client.post(
            '/api/auth/login/',
            data,
            format='json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)

    def test_login_invalid(self):
        User.objects.create_user(
            'user2',
            password='correct'
        )

        response = self.client.post(
            '/api/auth/login/',
            {
                'username': 'user2',
                'password': 'wrong'
            },
            format='json'
        )

        self.assertEqual(response.status_code, 401)


class TaskTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            'taskuser',
            password='Pass@1234'
        )

        self.token = Token.objects.create(
            user=self.user
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )

    def test_create_task(self):
        data = {
            'title': 'Test Task',
            'priority': 'high'
        }

        response = self.client.post(
            '/api/tasks/',
            data,
            format='json'
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(
            Task.objects.first().owner,
            self.user
        )

    def test_list_tasks(self):
        Task.objects.create(
            title='Task A',
            owner=self.user
        )

        Task.objects.create(
            title='Task B',
            owner=self.user
        )

        response = self.client.get('/api/tasks/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)

    def test_unauthenticated_access(self):
        client = APIClient()

        response = client.get('/api/tasks/')

        self.assertEqual(response.status_code, 401)

    def test_user_cannot_see_other_users_tasks(self):
        other_user = User.objects.create_user(
            'other',
            password='Pass@1234'
        )

        Task.objects.create(
            title='Other Task',
            owner=other_user
        )

        response = self.client.get('/api/tasks/')

        self.assertEqual(
            response.data['count'],
            0
        )