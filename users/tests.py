from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class UserTestCase(APITestCase):
    """ Tests all actions related to users
        
        Variables:
        user_data: user login information
    """
    
    user_data = None

    def setUp(self):
        """ Setting up a user account to use later in the login tests """
        self.user = User.objects.create_user(
            username="test.user", email="test.user@django.com",
            password="strong_password")
        self.user_data = {
            "username": "test.user", "email":"test.user@django.com",
            "password": "strong_password"}

    def test_registration(self):
        """ Testing user registration
            First, it tries to register the user, and then checks two
            factors:
                If the returned status code is HTTP 201 CREATED, and
                if the user was added to the database
        """
        data = {
            "username": "test.registration",
            "email": "test.registration@django.com",
            "password": "strong_password"}
        response = self.client.post('/users/registration/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.get(
            username='test.registration'))
    
    def test_login(self):
        """ Testing user login in three different ways:
            With wrong username and then with the wrong password, checking the 
            response status expecting a HTTP 401 UNAUTHORIZED for both cases.
            Finally, with correct username and password, expecting the
            response status to return a HTTP 200 OK
        """
        # testing with the wrong username
        data = {"username": "wrong.username", "password": "strong_password"}
        response = self.client.post('/users/login/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # testing with the wrong password
        data = {"username": "test.user", "password": "wrong_password"}
        response = self.client.post('/users/login/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # testing with the correct username and password
        response = self.client.post('/users/login/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_login_token(self):
        """ Testing if login is returning JWT tokens """
        response = self.client.post('/users/login/', self.user_data)
        self.assertTrue('refresh' in response.data)
        self.assertTrue('access' in response.data)
    
    def test_login_token_refresh(self):
        """ Testing if it's possible to refresh an expired token """
        response = self.client.post('/users/login/', self.user_data)
        token_refresh = response.data['refresh']
        response = self.client.post(
            '/users/login/refresh/', {"refresh": token_refresh})
        self.assertTrue('access' in response.data)
