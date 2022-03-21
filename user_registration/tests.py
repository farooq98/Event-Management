from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class UserRegistrationTest(APITestCase):

    def setUp(self):
        url = reverse('user_registration:register')
        data = {
            "username": "farooq",
            "email": "farooq@gmail.com",
            "mobile_number": "03123456710",
            "password": "sastaticket9578"
        }
        self.client.post(url, data, format='json')

    def test_user_registration(self):
        url = reverse('user_registration:register')
        data = {
            "username": "farooq2",
            "email": "farooq2@gmail.com",
            "mobile_number": "03123456789",
            "password": "sastaticket9578"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_creation_failed(self):

        url = reverse('user_registration:register')
        data = {
            "username": "farooq",
            "email": "farooq@gmail.com",
            "mobile_number": "03123456710",
            "password": "sastaticket9578"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data.pop("username")
        expected_response = {
            "mobile_number": [
                "user with this mobile number already exists."
            ],
            "username": [
                "This field is required."
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected_response)
    
    def test_login(self):
        url = reverse('user_registration:login')
        data = {
            "username": "farooq",
            "password": "sastaticket9578"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_failed(self):

        url = reverse('user_registration:login')
        data = {
            "username": "farooq",
            "password": "wrongpassword"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
