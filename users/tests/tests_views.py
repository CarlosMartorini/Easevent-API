from django.test import TestCase
from rest_framework.test import APIClient

class UserAccountViewsTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        self.artist1_data = {
            "username": 'Lady Gaga',
            "password": '1234',
            "email": 'ladygaga@gmail.com',
            "is_superuser": False,
            "phone": '23995465422',
            "solo": True,
            "hour_price": 200,
        }

        self.artist1_login_data = {
            "username": 'Lady Gaga',
            "password": '1234',
        }

        self.wrong_artist1_login_data = {
            "username": 2,
            "password": '1234'
        }

        self.owner_event1_data = {
            "username": 'Kate Bishop',
            "password": '1234',
            "email": 'ladygaga@gmail.com',
            "is_superuser": True,
        }

        self.owner_event1_login_data = {
            "username": 'Kate Bishop',
            "password": '1234',
        }

        self.wrong_artist1_data = {
            "username": 'Lady Gaga',
            "password": '1234',
            "is_superuser": False,
            "phone": '23995465422',
            "solo": True,
            "hour_price": 200,
            # missing email
        }
        self.wrong_owner_event1_data = {
            "username": 'Kate Bishop',
            "password": '1234',
            "email": 'ladygaga@gmail.com',
            # missing is_superuser
        }

        self.wrong_artist1_login_data_1 = {
            "username": 2,
            "password": '1234'
            # incorrect type value
        }
        self.wrong_artist1_login_data_2 = {
            "username": 'ASDASDDA',
            "password": '1234'
            # incorrect credentials
        }


    def test_create_an_artist_successfully_and_login_is_working(self):

        # CREATE AN ARTIST
        response = self.client.post('/api/accounts/', self.artist1_data, format='json')
        self.assertEqual(response.status_code, 201)

        artist1_copy = self.artist1_data.copy()
        artist1_copy.pop('password')

        self.assertEqual(response.json(),
                         {
                            'id': 1,
                            **self.artist1_copy
                          }
                         )


        # LOGIN AS ARTIST
        logged_user = self.client.post('/api/login/', self.artist1_login_data, format='json')

        self.assertIn('token', logged_user.keys())

        self.assertEqual(logged_user.status_code, 200)

    def test_create_an_owner_successfully_and_login_is_working(self):

        # CREATE AN OWNER_EVENT
        response = self.client.post('/api/accounts/', self.owner_event1_data, format='json')

        self.assertEqual(response.status_code, 201)

        owner1_copy = self.owner_event1_data.copy()
        owner1_copy.pop('password')

        self.assertEqual(response.json(),
                         {
                            'id': 1,
                            **self.owner1_copy
                          }
                         )


        # LOGIN AS OWNER_EVENT
        logged_user = self.client.post('/api/login/', self.owner_event1_login_data, format='json')

        self.assertIn('token', logged_user.keys())

        self.assertEqual(logged_user.status_code, 200)


    def test_fail_to_create_an_artist_when_missing_data(self):

        # CREATE AN ARTIST
        response = self.client.post('/api/accounts/', self.wrong_artist1_data, format='json')

        self.assertEqual(response.status_code, 406)

    def test_fail_to_create_an_owner_when_missing_data(self):
        # CREATE AN OWNER_EVENT
        response = self.client.post('/api/accounts/', self.wrong_owner_event1_data, format='json')

        self.assertEqual(response.status_code, 406)

    def test_create_an_user_successfully_but_type_of_any_field_of_login_is_invalid(self):

        # CREATE AN ARTIST
        self.client.post('/api/accounts/', self.artist1_data, format='json')

        # LOGIN AS ARTIST
        logged_user = self.client.post('/api/login/', self.wrong_artist1_login_data_1, format='json')

        self.assertNotIn('token', logged_user.keys())

        self.assertEqual(logged_user.status_code, 422)

    def test_create_an_user_successfully_but_login_fall_with_wrong_credentials_value(self):

        # CREATE AN ARTIST
        self.client.post('/api/accounts/', self.artist1_data, format='json')

        # LOGIN AS ARTIST
        logged_user = self.client.post('/api/login/', self.wrong2_artist1_login_data_2, format='json')

        self.assertNotIn('token', logged_user.keys())

        self.assertEqual(logged_user.status_code, 401)