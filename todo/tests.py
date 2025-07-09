from django.test import TestCase, Client
from django.utils import timezone
from datetime import datetime
from django.urls import reverse
from todo.models import Task

class TaskModelTestCase(TestCase):
    def test_create_task_with_due(self):
        due = timezone.make_aware(datetime(2024, 6, 30, 23, 59, 59))
        task = Task(title='task1', due_at=due)
        task.save()

        saved = Task.objects.get(pk=task.pk)
        self.assertEqual(saved.title, 'task1')
        self.assertFalse(saved.completed)
        self.assertEqual(saved.due_at, due)

    def test_create_task_without_due(self):
        task = Task(title='task2')
        task.save()

        saved = Task.objects.get(pk=task.pk)
        self.assertEqual(saved.title, 'task2')
        self.assertFalse(saved.completed)
        self.assertIsNone(saved.due_at)

    def test_is_overdue_future(self):
        due = timezone.make_aware(datetime(2024, 6, 30, 23, 59, 59))
        current = timezone.make_aware(datetime(2024, 6, 30, 0, 0, 0))
        task = Task(title='task1', due_at=due)
        task.save()

        self.assertFalse(task.is_overdue(current))

class TaskViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_get_empty(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'todo/index.html')
        self.assertEqual(len(response.context['tasks']), 0)

    def test_index_post_creates_task(self):
        data = {
            'title': 'Test Task',
            'description': 'test description',
            'due_at': datetime(2025, 7, 9, 12, 0, 0).isoformat()
        }
        response = self.client.post(reverse('index'), data)
        self.assertIn(response.status_code, (200, 302))
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(response.templates[0].name, 'todo/index.html')

    def test_index_get_order_posted_desc(self):
        older = Task(title='older', due_at=timezone.now())
        older.save()
        newer = Task(title='newer', due_at=timezone.now())
        newer.save()

        response = self.client.get(reverse('index'))
        self.assertEqual(response.context['tasks'][0], newer)
        self.assertEqual(response.context['tasks'][1], older)

    def test_index_get_order_due_asc(self):
        first = Task(title='first', due_at=timezone.make_aware(datetime(2024, 7, 1)))
        first.save()
        second = Task(title='second', due_at=timezone.make_aware(datetime(2024, 8, 1)))
        second.save()

        response = self.client.get(reverse('index') + '?order=due')
        self.assertEqual(response.context['tasks'][0], first)
        self.assertEqual(response.context['tasks'][1], second)
    
class TodoViewTestCase(TestCase):
    def test_detail_success(self):
        task = Task(title='task1', due_at=timezone.make_aware(datetime(2024, 7, 1)))
        task.save()
        client = Client()


        response = client.get('/{}/'.format(task.pk))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['task'], task)
        self.assertEqual(response.templates[0].name, 'todo/detail.html')
    
    def test_dtail_get_fail(self):
        client = Client()
        response = client.get('/1/')
        
        self.assertEqual(response.status_code, 404)