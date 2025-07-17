import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from product.models import Category
from django.contrib.auth.models import User


class CategoryTests(APITestCase):
    fixtures = ['categories']

    def setUp(self):

        self.user=User.objects.create_user(username='useradmin',password='Rootroot')
        self.staff_user = User.objects.create_user(username='staffuser',password='root')
        self.client.force_authenticate(user=self.user)
        self.category1=Category.objects.first()


    def test_category_list(self):
        url=reverse('category-list')
        response=self.client.get(url)

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),4)

    def test_detail(self):
        url=reverse('category-detail',args=[self.category1.id])
        response=self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_category_create(self):
        url=reverse('category-list')
        data={'name':'Mac'}
        response=self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_category_update(self):
        url=reverse('category-detail',args=[self.category1.id])
        data={'name':'Macos'}
        response=self.client.put(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_category_delete(self):
        url=reverse('category-detail',args=[self.category1.id])
        response=self.client.delete(url)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

    def test_user_without_permission(self):
        self.client.force_authenticate(user=None)
        url=reverse('user-list')
        response=self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
