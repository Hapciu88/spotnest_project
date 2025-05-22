from django.test import TestCase, Client
from django.urls import reverse

# Create your tests here.

class PagesModuleTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_landing_page_loads(self):
        response = self.client.get(reverse('module_pages:home'))
        self.assertEqual(response.status_code, 200)
