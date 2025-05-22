from django.test import TestCase, Client
from django.urls import reverse
from users_module.models import CustomUser
from .models import Property, PropertyRequest

# Create your tests here.

class PropertyModuleTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.landlord = CustomUser.objects.create_user(username='landlord', password='pass', user_type='landlord')
        self.tenant = CustomUser.objects.create_user(username='tenant', password='pass', user_type='tenant')
        self.property = Property.objects.create(
            landlord=self.landlord,
            title='Test Property',
            description='Test Desc',
            rental_price=1000,
            address='123 Test St',
            latitude=0.0,
            longitude=0.0
        )

    def test_property_detail_view(self):
        response = self.client.get(reverse('module_property:property_detail', args=[self.property.id]))
        self.assertEqual(response.status_code, 200)

    def test_tenant_can_request_property(self):
        self.client.login(username='tenant', password='pass')
        response = self.client.post(reverse('module_property:property_detail', args=[self.property.id]), {'request_submit': '1'})
        self.assertEqual(PropertyRequest.objects.count(), 1)
        self.assertEqual(PropertyRequest.objects.first().tenant, self.tenant)
