<<<<<<< HEAD
from rest_framework.reverse import reverse
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from django.urls import path, include, re_path
from rest_framework.utils import json

from quiz.serializers import QuizSerializer
from user.models import Profile
from quiz.models import Quiz, QuizResult
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
            'email': 'Muffin@mail.ru'
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
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_profile(self):
        response = client.post(
            'http://127.0.0.1:8000/api/auth/users/',
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleProfileTest(TestCase):
    """ Test module for updating an existing puppy record """
    def setUp(self):
        self.casper = Profile.objects.create(username='Casper', password='password213', email='Casper@mail')
        self.muffin = Profile.objects.create(username='Muffin', password='password321', email='Muffin@mail')
        self.valid_payload = {
            'username': 'Muffin',
            'password': 'password213',
            'email': 'Muffin@mail.ru'
        }
        self.invalid_payload = {
            'username': '',
            'password': '',
            'email': ''
        }

    def test_valid_update_profile(self):
        response = client.put(
            reverse('get_update_profile', kwargs={'pk': self.muffin.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_profile(self):
        response = client.put(
            reverse('get_update_profile', kwargs={'pk': self.muffin.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
=======
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, URLPatternsTestCase


class AccountTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('', include('quizsite.urls')),
    ]
    print(urlpatterns)
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('quiz')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
>>>>>>> f878692612f0864d305775c963d16d14f3e04169
