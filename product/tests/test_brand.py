import os
import django
from rest_framework import status

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.urls import reverse
from rest_framework.test import APITestCase
from product.models import Brand
from django.contrib.auth.models import User

class BrandTests(APITestCase):
    fixtures = ['brands']

    def setUp(self):

        self.user=User.objects.create_user(username='admin1',password='root')
        self.staff_user=User.objects.create_user(username='staffuser',password='root')
        self.client.force_authenticate(user=self.user)
        self.brand1=Brand.objects.first()

    def test_brand_list(self):
        url = reverse('brand-list')
        response=self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 4)

    def test_brand_create(self):
        url=reverse('brand-list')
        data={
            'name':'Artel'
        }
        response=self.client.post(url,data,format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_brand_update(self):
        url=reverse('brand-detail',args=[self.brand1.pk])
        data={
            'name':'Samsung'
        }
        response=self.client.put(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['name'],'Samsung')

    def test_brand_delete(self):
        # self.client.force_authenticate(user=self.staff_user)
        url=reverse('brand-detail',args=[self.brand1.pk])
        response=self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthorized_user(self):
        self.client.force_authenticate(user=None)
        url=reverse('brand-list')
        response=self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)