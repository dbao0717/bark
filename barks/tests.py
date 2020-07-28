from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import Bark

User = get_user_model()
class BarkTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username = 'def', password = '123456')
        self.user2 = User.objects.create_user(username = 'def-2', password = '123456')
        Bark.objects.create(content = "my first bark", user = self.user)
        Bark.objects.create(content = "my second bark", user = self.user)
        Bark.objects.create(content = "my third bark", user = self.user2)
        self.currentCount = Bark.objects.all().count()

    def test_bark_created(self):
        bark_obj = Bark.objects.create(content = "my fourth bark", user = self.user)
        self.assertEqual(bark_obj.id, 4)
        self.assertEqual(bark_obj.user, self.user)

    def get_client(self):
        client = APIClient()
        client.login(username = self.user.username, password = '123456')
        return client

    def test_bark_list(self):
        client = self.get_client()
        response = client.get("/api/barks/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    def test_barks_related_name(self):
        user = self.user
        self.assertEqual(user.barks.count(), 2)


    def test_action_like(self):
        client = self.get_client()
        response = client.post("/api/barks/action/", {"id": 1, "action": "like"})
        like_count = response.json().get("likes")
        user = self.user
        my_like_instances = user.barklike_set.count()
        my_related_likes = user.bark_user.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(like_count, 1)
        self.assertEqual(my_like_instances, 1)
        self.assertEqual(my_like_instances, my_related_likes)


    def test_action_unlike(self):
        client = self.get_client()
        response = client.post("/api/barks/action/", {"id": 1, "action": "like"})
        self.assertEqual(response.status_code, 200)
        response = client.post("/api/barks/action/", {"id": 1, "action": "unlike"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 0)

    def test_action_rebark(self):
        client = self.get_client()
        response = client.post("/api/barks/action/", {"id": 2, "action": "rebark"})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        new_bark_id = data.get("id")
        self.assertNotEqual(2, new_bark_id)
        self.assertEqual(self.currentCount + 1, new_bark_id)

    def test_bark_create_api_view(self):
        request_data = {"content": "this is a test bark"}
        client = self.get_client()
        response = client.post("/api/barks/create/", request_data)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        new_bark_id = response_data.get("id")
        self.assertEqual(self.currentCount + 1, new_bark_id)

    def test_bark_detail_api_view(self):
        client = self.get_client()
        response = client.get("/api/barks/1/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        bark_id = data.get("id")
        self.assertEqual(bark_id, 1)

    def test_bark_delete_api_view(self):
        client = self.get_client()
        response = client.delete("/api/barks/1/delete/")
        self.assertEqual(response.status_code, 200)
        response = client.delete("/api/barks/1/delete/")
        self.assertEqual(response.status_code, 404)
        response_incorrect_owner = client.delete("/api/barks/3/delete/")
        self.assertEqual(response_incorrect_owner.status_code, 401)