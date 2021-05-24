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

    def test_user(self):
        user_data = {
            "email": "user2@user.com",
            "name": "User2",
            "password": "user2"
        }

        user = User.objects.create_user(
            email=user_data["email"],
            name=user_data["name"],
            password=user_data["password"]
        )
        self.assertEqual(user.is_active, 1, 'Active user')

        response = self.client.post(reverse("token_obtain_pair"), self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

        access_token = response.data["access"]
        client = APIClient()

        client.credentials(HTTP_AUTHORIZATION="JWT %s" %access_token)
        response = client.get(reverse("user_profile"), data={"format": "json"})
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

    def test_wrong_token(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="JWT 123456789")
        response = client.get(reverse("user_profile"), data={"format": "json"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_userlist(self):
        superuser_data = {
            "email": "user3@user.com",
            "name": "SuperUser",
            "password": "user3"
        }

        superuser = User.objects.create_superuser(
            email=superuser_data["email"],
            name=superuser_data["name"],
            password=superuser_data["password"]
        )
        self.assertEqual(superuser.is_superuser, 1, 'Active superuser')

        response = self.client.post(reverse("token_obtain_pair"), superuser_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

        superuser_access_token = response.data["access"]
        client = APIClient()
        
        client.credentials(HTTP_AUTHORIZATION="JWT %s" %superuser_access_token)
        response = client.get(reverse("user_list"), data={"format": "json"})
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)