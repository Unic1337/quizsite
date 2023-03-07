from rest_framework.reverse import reverse
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.utils import json


from user.models import Profile
from user.serializers import ProfileSerializer

client = Client()


class GetAllProfilesTest(TestCase):
    """ Test module for GET all profiles API """
    def setUp(self):
        Profile.objects.create(username='Casper', password='password213', email="Casper@mail")
        Profile.objects.create(username='Muffin', password='password321', email="Muffin@mail")
        Profile.objects.create(username='Rambo', password='password123', email="Rambo@mail")

    def test_get_all_puppies(self):
        response = client.get('http://127.0.0.1:8000/api/auth/users/')
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleProfilesTest(TestCase):
    """ Test module for GET single profile API """
    def setUp(self):
        self.casper = Profile.objects.create(username='Casper', password='password213', email='Casper@mail')
        self.muffin = Profile.objects.create(username='Muffin', password='password321', email='Muffin@mail')
        self.rambo = Profile.objects.create(username='Rambo', password='password123', email='Rambo@mail')

    def test_get_valid_single_profile(self):
        response = client.get(reverse('get_update_profile', kwargs={'pk': self.rambo.pk}))
        profile = Profile.objects.get(pk=self.rambo.pk)
        serializer = ProfileSerializer(profile)
        self.assertEqual(response.data["profile"], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_profile(self):
        response = client.get(
            reverse('get_update_profile', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewProfileTest(TestCase):
    """ Test module for inserting a new puppy """
    def setUp(self):
        self.valid_payload = {
            'username': 'Muffin',
            'password': 'password213',
            'email': 'Muffin@mail.ru',
        }
        self.invalid_payload = {
            'username': '',
            'password': '',
            'email': ''
        }

    def test_create_valid_profile(self):
        response = client.post(
            'http://127.0.0.1:8000/api/auth/users/',
            data=json.dumps(self.valid_payload),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_profile(self):
        response = client.post(
            'http://127.0.0.1:8000/api/auth/users/',
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
