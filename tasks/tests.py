from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Task

# Create your tests here.

class TaskAPITestCase(APITestCase):

    def test_create_task(self):
        url = reverse('task-list')
        data = {'title': 'Test Task', 'description': 'Description of test task'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)

    def test_list_tasks(self):
        Task.objects.create(title='Task 1', is_completed=True)
        Task.objects.create(title='Task 2', is_completed=False)
        url = reverse('task-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_task(self):
        task = Task.objects.create(title='Initial Title', is_completed=False)
        url = reverse('task-detail', args=[task.id])
        data = {'title': 'Updated Title', 'is_completed': True}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, 'Updated Title')
        self.assertTrue(task.is_completed)

    def test_delete_task(self):
        task = Task.objects.create(title='Task to Delete')
        url = reverse('task-detail', args=[task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
