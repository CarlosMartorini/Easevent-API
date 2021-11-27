from django.test import TestCase
from rest_framework.test import APIClient

class UserAccountViewsTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        self.artist1_data = {
            "username": 'LadyGaga',
            "password": '1234',
            "email": 'ladygaga@gmail.com',
            "is_superuser": False,
            "phone": '23995465422',
            "solo": True,
            "hour_price": 200,
        }

        self.artist1_login_data = {
            "username": 'LadyGaga',
            "password": '1234',
        }

        self.wrong_artist1_login_data = {
            "username": 2,
            "password": '1234'
        }

        self.owner_event1_data = {
            "username": 'KateBishop',
            "password": '1234',
            "email": 'ladygaga@gmail.com',
            "is_superuser": True,
        }

        self.owner_event1_login_data = {
            "username": 'KateBishop',
            "password": '1234',
        }

        self.wrong_artist1_data = {
            "username": 'LadyGaga',
            "password": '1234',
            "is_superuser": False,
            "phone": '23995465422',
            "solo": True,
            "hour_price": 200,
            # missing email
        }
        self.wrong_owner_event1_data = {
            "username": 'KateBishop',
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
                            **artist1_copy
                          }
                         )


        # LOGIN AS ARTIST
        logged_user = self.client.post('/api/login/', self.artist1_login_data, format='json')

        self.assertIn('token', logged_user.json().keys())

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
                            **owner1_copy
                          }
                         )


        # LOGIN AS OWNER_EVENT
        logged_user = self.client.post('/api/login/', self.owner_event1_login_data, format='json')

        self.assertIn('token', logged_user.json().keys())

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

        self.assertNotIn('token', logged_user.json().keys())

        self.assertEqual(logged_user.status_code, 415)

    def test_create_an_user_successfully_but_login_fall_with_wrong_credentials_value(self):

        # CREATE AN ARTIST
        self.client.post('/api/accounts/', self.artist1_data, format='json')

        # LOGIN AS ARTIST
        logged_user = self.client.post('/api/login/', self.wrong_artist1_login_data_2, format='json')

        self.assertNotIn('token', logged_user.json().keys())

        self.assertEqual(logged_user.status_code, 401)

    def test_get_all_users(self):
        artist = self.client.post('/api/accounts/', self.artist1_data, format='json')
        self.assertEqual(artist.status_code, 201)

        owner = self.client.post('/api/accounts/', self.owner_event1_data, format='json')
        self.assertEqual(owner.status_code, 201)

        users = self.client.get('/api/accounts/', format='json')
        self.assertEqual(len(users.json()), 2)
        self.assertEqual(users.status_code, 200)

    def test_update_own_profile_info(self):
        artist = self.client.post('/api/accounts/', self.artist1_data, format='json')
        self.assertEqual(artist.status_code, 201)

        response = self.client.put('/api/accounts/1/', {'username': 'TaylorSwift'}, format='json')
        self.assertEqual(response.status_code, 200)


        expected_data = self.artist1_data.copy()
        expected_data['username'] = 'TaylorSwift'

        self.assertEqual(response.json().keys(),
                            {
                                'id': 1,
                                **expected_data
                            }
                         )

        self.assertEqual(len(response.json()), 1)

    def test_fail_to_update_own_profile_info_because_id_not_found(self):
        response = self.client.put('/api/accounts/1/', {'username': 'TaylorSwift'}, format='json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'error': 'User not founded'})

