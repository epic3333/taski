from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Task


class TaskModelTest(APITestCase):
    def test_task_str(self):
        task = Task(title='Test task')
        self.assertEqual(str(task), 'Test task')

    def test_task_default_status(self):
        task = Task.objects.create(title='Test task')
        self.assertEqual(task.status, Task.NEW)


class TaskAPITest(APITestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title='Test task',
            description='Test description',
            status=Task.NEW,
        )
        self.list_url = reverse('task-list')
        self.detail_url = reverse('task-detail', args=[self.task.pk])

    def test_list_tasks(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_task(self):
        data = {'title': 'New task', 'description': 'Desc', 'status': Task.NEW}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(response.data['title'], 'New task')

    def test_retrieve_task(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.task.title)

    def test_update_task(self):
        data = {'title': 'Updated', 'description': 'Updated desc', 'status': Task.DONE}
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated')
        self.assertEqual(self.task.status, Task.DONE)

    def test_partial_update_task(self):
        response = self.client.patch(
            self.detail_url, {'status': Task.IN_PROGRESS}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, Task.IN_PROGRESS)

    def test_delete_task(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_create_task_missing_title(self):
        response = self.client.post(self.list_url, {'description': 'No title'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
