import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from product.models import *
from django.contrib.auth.models import User


class CategoryTest(APITestCase):

    def setUp(self):
        self.user1=User.objects.create_user(username='admin1',password='root')
        self.user2=User.objects.create_user(username='admin2',password='root')
        self.user3=User.objects.create_user(username='admin3',password='root')
        self.staff_user=User.objects.create_user(password='rootstaff',username='staffuser',is_staff=True)

        self.brand1=Brand.objects.create(name='Samsung')
        self.brand2=Brand.objects.create(name='Artel')
        self.brand3=Brand.objects.create(name='Samsung')

        self.category1=Category.objects.create(name='Telefonlar')
        self.category2=Category.objects.create(name='Televizorlar')
        self.category3=Category.objects.create(name='Noutbuklar')

        self.product1=Product.objects.create(title='S 23 ultra',description='S 23 Ultra',brand=self.brand1,category=self.category1,price=800,stock=100)
        self.product2=Product.objects.create(title='Artel',description='Artel display size 32',brand=self.brand2,category=self.category2,price=500,stock=200)
        self.product3=Product.objects.create(title='Acer Nitro',description='Acer Nitro 1 TB / 24 GB Memory',brand=self.brand3,category=self.category3,price=1200,stock=100)

        Review.objects.create(product=self.product1,rating=4,user=self.user1)
        Review.objects.create(product=self.product2,rating=5,user=self.user2)
        Review.objects.create(product=self.product3,rating=4,user=self.user3)
        Review.objects.create(product=self.product1,rating=3,user=self.user3)
        Review.objects.create(product=self.product1,rating=5,user=self.user3)
    def test_product_list(self):
        url=reverse('product-list')
        self.client.force_authenticate(self.user1)
        response=self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),4)

    def test_product_create(self):
        url=reverse('product-list')
        self.client.force_authenticate(self.user2)
        data = {
            'title': 'S 24',
            'description': 'updated desc',
            'brand': self.brand1.id,
            'category': self.category1.id,
            'price': 700,
            'stock': 100
        }
        response=self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_product_update(self):
        url=reverse('product-detail',args=[self.product1.id])
        self.client.force_authenticate(self.user1)
        data = {
            'title': 'S 24',
            'description': 'updated desc',
            'brand': self.brand1.id,
            'category': self.category1.id,
            'price': 700,
            'stock': 100
        }
        response=self.client.put(url,data,format="json")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'S 24')

    def test_product_delete(self):
        url=reverse('product-detail',args=[self.product1.id])
        self.client.force_authenticate(self.user1)

        response=self.client.delete(url)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

    def test_product_top_rated(self):
        url=reverse('product-top-rated')
        self.client.force_authenticate(self.user1)
        response=self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[2]['title'],'Artel')

    def test_product_retrieve(self):
        url=reverse('product-detail',args=[self.product1.id])
        self.client.force_authenticate(self.user2)
        data={'title':'S 23'}
        response=self.client.patch(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['title'],'S 23')

    def test_product_average_rating(self):
        url=reverse('product-average-rating',args=[self.product1.id])
        self.client.force_authenticate(self.user1)
        response=self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['average_rating'],4)

    def test_user_without_permission(self):
        self.client.force_authenticate(user=None)
        url=reverse('product-list')
        data={'title':'S 23 ultra','description':'S 23 Ultra','brand':self.brand1.id,'category':self.category1.id,'price':'800','stock':'100'}
        response=self.client.post(url,data,format="json")
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)



    def tearDown(self):
        User.objects.all().delete()