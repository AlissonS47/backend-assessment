from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Request


class ProjectTestCase(APITestCase):
    """ Tests all actions related to requests
        
        Variables:
        user_token: super user access token
        user2: regular user
        user2_token: regular user access token
        request_id: test request id
    """
    
    user_token = None
    user2 = None
    user2_token = None
    request_id = None

    def setUp(self):
        """ Setting up of a super user and a regular user to verify 
            authentication later 
        """
        # super user
        self.user = User.objects.create_user(
            username="super.user", email="super.user@django.com",
            password="strong_password", is_staff=True)
        data = {
            "username": "super.user", "email":"super.user@django.com",
            "password": "strong_password"}
        response = self.client.post('/users/login/', data)
        self.user_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')

        # regular user
        self.user2 = User.objects.create_user(
            username="test.user", email="test.user@django.com",
            password="strong_password")
        data = {
            "username": "test.user", "email":"test.user@django.com",
            "password": "strong_password"}
        response = self.client.post('/users/login/', data)
        self.user2_token = response.data['access']

        # test request
        test_request = Request.objects.create(
            user=self.user2, message='test request')
        test_request.save()
        self.request_id = test_request.id
    
    def test_auth(self):
        """ Checking endpoint permission, without authentication, checking the
            response status expecting a HTTP 401 UNAUTHORIZED, and wtih
            authentication, expecting a HTTP 200 OK
        """
        # without authentication
        self.client.credentials(HTTP_AUTHORIZATION='No Auth')
        response = self.client.get('/requests/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # with authentication
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user2_token}')
        response = self.client.get('/requests/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_registration(self):
        """ Testing request registration
            First, it tries to register the request, and then checks two
            factors:
                If the returned status code is HTTP 201 CREATED, and
                if the request was added to the database
        """
        data = {
            "message": "test request registration"
        }
        response = self.client.post('/requests/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Request.objects.get(
            message='test request registration'))
    
    def test_retrieve(self):
        """ Testing request retrive, expecting the test request """
        response = self.client.get(f'/requests/{self.request_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)
        self.assertEqual(dict(response.data)['message'], 'test request')

    def test_update(self):
        """ Testing request update in two different ways:
            With a regular user, checking the response status expecting a 
            HTTP 401 UNAUTHORIZED.
            With a super user, expecting a HTTP 200 OK and verifying that the 
            request has changed.
        """
        # data for update
        data = {
            "status": 'A'
        }
        
        # regular user trying to partial update the request
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.user2_token}')
        response = self.client.patch(
            f'/requests/{self.request_id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # super user trying to partial update the request
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        response = self.client.patch(
            f'/requests/{self.request_id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            Request.objects.get(id=self.request_id).status == 'A')
    
    def test_delete(self):
        """ Testing request delete in two different ways:
            With a super user, checking the response status expecting a 
            HTTP 401 UNAUTHORIZED.
            With the owner user, expecting a HTTP 200 OK and verifying that 
            the request was deleted.
        """
        # super user trying to delete the request
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        response = self.client.delete(
            f'/requests/{self.request_id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(
            Request.objects.filter(id=self.request_id).exists())
        
        # owner user trying to delete the request
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.user2_token}')
        response = self.client.delete(
            f'/requests/{self.request_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            Request.objects.filter(id=self.request_id).exists())
        
