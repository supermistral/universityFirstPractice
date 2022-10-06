from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import User


class UsersViewsTests(APITestCase):
    def setUp(self):
        self.email = "user2@user.com"
        self.password = "user2"
        self.name = "User2"
        self.is_staff = False
        self.data = {
            "email": self.email,
            "password": self.password
        }
        self.superuser_data = {
            "email": "user3@user.com",
            "name": "SuperUser",
            "password": "user3"
        }
    
    def create_user(self):
        return User.objects.create_user(
            email=self.email,
            name=self.name,
            password=self.password
        )

    def create_superuser(self):
        return User.objects.create_superuser(
            email=self.superuser_data["email"],
            name=self.superuser_data["name"],
            password=self.superuser_data["password"]
        )

    def test_create_user(self):
        user = self.create_user()

        self.assertEqual(user.is_active, 1)
        self.assertEqual(user.is_superuser, 0)
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.check_password(self.password), True)
    
    def test_create_superuser(self):
        superuser = self.create_superuser()

        self.assertEqual(superuser.is_active, 1)
        self.assertEqual(superuser.is_superuser, 1) 
        self.assertEqual(superuser.email, self.superuser_data['email'])
        self.assertEqual(superuser.check_password(self.superuser_data['password']), True)

    def test_user_token(self):
        user = self.create_user()
        response = self.client.post(reverse("token_obtain_pair"), self.data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual('user' in response.data, True)
        self.assertEqual('name' in response.data['user'] and 'is_staff' in response.data['user'], True)
        self.assertEqual(response.data['user']['name'], self.name)
        self.assertEqual(response.data['user']['is_staff'], False)
    
    def test_user_permssions(self):
        user = self.create_user()

        response = self.client.post(reverse("token_obtain_pair"), self.data, format="json")
        access_token = response.data["access"]

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="JWT %s" % access_token)

        response = client.get(reverse("user_profile"), data={"format": "json"})
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(response.data['name'], self.name)

        response = client.get(reverse("user_list"), data={"format": "json"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)

    def test_unauthorized_client(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="JWT 123456789")

        response = client.get(reverse("user_profile"), data={"format": "json"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.content)

    def test_superuser_token(self):
        user = self.create_superuser()

        response = self.client.post(reverse("token_obtain_pair"), self.superuser_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(response.data['user']['name'], self.superuser_data['name'])
        self.assertEqual(response.data['user']['is_staff'], True)
    
    def test_superuser_permissions(self):
        user = self.create_superuser()

        response = self.client.post(reverse("token_obtain_pair"), self.superuser_data, format="json")
        access_token = response.data["access"]

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="JWT %s" % access_token)

        response = client.get(reverse("user_list"), data={"format": "json"})
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
