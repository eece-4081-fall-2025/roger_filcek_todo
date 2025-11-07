from django.test import TestCase
from django.urls import reverse
from .models import Task

class TaskModelTests(TestCase):
    def test_create_task_str(self):
        task = Task.objects.create(title="Test Task")
        self.assertEqual(str(task), "Test Task")


class TaskViewTests(TestCase):
    def setUp(self):
        self.task = Task.objects.create(title="Sample Task", details="Details")

    def test_task_list_view_loads(self):
        response = self.client.get(reverse("task_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sample Task")

    def test_create_task_success(self):
        response = self.client.post(reverse("task_create"), {"title": "New Task"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title="New Task").exists())

    def test_edit_updates_title(self):
        response = self.client.post(reverse("task_update", args=[self.task.pk]), {"title": "Edited Task"})
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Edited Task")

    def test_complete_requires_post(self):
        response = self.client.get(reverse("task_complete", args=[self.task.pk]))
        self.assertEqual(response.status_code, 405) 

    def test_archive_hides_from_list(self):
        self.client.post(reverse("task_archive", args=[self.task.pk]))
        response = self.client.get(reverse("task_list"))
        self.assertNotContains(response, "Sample Task")

    def test_archive_twice_returns_404(self):
        self.client.post(reverse("task_archive", args=[self.task.pk]))
        second = self.client.post(reverse("task_archive", args=[self.task.pk]))
        self.assertEqual(second.status_code, 404)
