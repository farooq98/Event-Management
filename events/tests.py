from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class UserRegistrationTest(APITestCase):

    def create_and_login_new_user(self, username, mobile_number):
        url = reverse('user_registration:register')
        register_payload = {
            "username": username,
            "email": "farooq2@gmail.com",
            "mobile_number": mobile_number,
            "password": "sastaticket9578"
        }
        self.client.post(url, register_payload, format='json')

        url = reverse('user_registration:login')
        Login_payload = {
            "username": register_payload['username'],
            "password": register_payload['password'],
        }
        self.client.post(url, Login_payload, format='json')

    def setUp(self):
        
        self.create_and_login_new_user("farooq", "03123456710")
        url = reverse('events:create_event')
        create_event_payload_1 = {
            "title": "Birthday Party",
            "description": "This is a birthday party",
            "date": "2022-03-23T07:30:15.109517Z",
            "location": "Avari"
        }
        response_1 = self.client.post(url, create_event_payload_1, format='json')

        url = reverse('events:create_event')
        create_event_payload_2 = {
            "title": "Convocation",
            "description": "This is a Convocation Event",
            "date": "2022-03-25T07:30:15.109517Z",
            "location": "PC"
        }
        response_2 = self.client.post(url, create_event_payload_2, format='json')

        self.event_ids = {
            response_1.json().get('id'): create_event_payload_1, 
            response_2.json().get('id'): create_event_payload_2,
        }

    def test_list_events(self):
        url = reverse('events:events_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get('results', [])), 2)

    def test_get_event(self):

        for event_id in self.event_ids.keys():
            url = reverse('events:event_details', kwargs={"id": event_id})
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_event(self):

        url = reverse('events:create_event')
        create_event_payload = {
            "title": "Convocation 2",
            "description": "This is a Convocation Event",
            "date": "2022-03-29T07:30:15.109517Z",
            "location": "PC 2"
        }
        response = self.client.post(url, create_event_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_event_failure(self):

        url = reverse('events:create_event')
        create_event_payload = {
            "description": "This is a Convocation Event",
            "date": "2022-03-29T07:30:15.109517Z",
            "location": "PC 2"
        }
        response = self.client.post(url, create_event_payload, format='json')
        expected_response = {
            "title": [
                "This field is required."
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected_response)

    def test_update_event(self):

        for event_id, data in self.event_ids.items():
            url = reverse('events:event_details', kwargs={"id": event_id})
            updated_data = {
                **data,
                "description": data['description'] + " updated"
            }
            response = self.client.put(url, updated_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json().get('description'), data['description'] + " updated")

    def test_update_event_failure(self):

        self.create_and_login_new_user("farooq2", "03123456598")
        for event_id, data in self.event_ids.items():
            url = reverse('events:event_details', kwargs={"id": event_id})
            updated_data = {
                **data,
                "description": data['description'] + " updated"
            }
            response = self.client.put(url, updated_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_event(self):

        for event_id in self.event_ids.keys():
            url = reverse('events:event_details', kwargs={"id": event_id})
            response = self.client.delete(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_event_failure(self):
    
        self.create_and_login_new_user("farooq2", "03123456598")
        for event_id in self.event_ids.keys():
            url = reverse('events:event_details', kwargs={"id": event_id})
            response = self.client.delete(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_attend_event(self):

        for event_id in self.event_ids.keys():
            url = reverse('events:create_attendees', kwargs={"id": event_id})
            response = self.client.post(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_attend_event(self):
        self.test_attend_event()
        for event_id in self.event_ids.keys():
            url = reverse('events:create_attendees', kwargs={"id": event_id})
            response = self.client.get(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.json().get("results", [])), 1)

    def test_attend_event_failure(self):

        url = reverse('user_registration:logout')
        self.client.post(url, format='json')

        for event_id in self.event_ids.keys():
            url = reverse('events:create_attendees', kwargs={"id": event_id})
            response = self.client.post(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)