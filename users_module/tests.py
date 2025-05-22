from django.test import TestCase, Client
from django.urls import reverse
from .models import CustomUser

# Create your tests here.

class UsersModuleTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.tenant = CustomUser.objects.create_user(username='tenant', password='pass', user_type='tenant')

    def test_signup_page_loads(self):
        response = self.client.get(reverse('module_users:signup'))
        self.assertEqual(response.status_code, 200)

    def test_signin_page_loads(self):
        response = self.client.get(reverse('module_users:signin'))
        self.assertEqual(response.status_code, 200)

    def test_profile_view(self):
        self.client.login(username='tenant', password='pass')
        response = self.client.get(reverse('module_users:profile_view'))
        self.assertEqual(response.status_code, 200)
