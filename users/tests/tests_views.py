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
            "hour_price": 200.0,
        }

        self.artist1_login_data = {
            "username": 'LadyGaga',
            "password": '1234',
        }

        self.artist2_data = {
            "username": 'Mamonas',
            "password": '1234',
            "email": 'mamonasassassinas@gmail.com',
            "is_superuser": False,
            "phone": '239215465422',
            "solo": False,
            "hour_price": 200.0,
        }

        self.artist2_login_data = {
            "username": 'Mamonas',
            "password": '1234',
        }


        self.wrong_artist1_login_data = {
            "username": 2,
            "password": '1234'
        }

        self.owner_event1_data = {
            "username": 'KateBishop',
            "password": '1234',
            "email": 'katebishop@gmail.com',
            "is_superuser": True,
        }

        self.owner_event1_login_data = {
            "username": 'KateBishop',
            "password": '1234',
        }

        self.owner_event2_data = {
            "username": 'HaileeSteinfeld',
            "password": '1234',
            "email": 'haileesteinfeld@gmail.com',
            "is_superuser": True,
        }

        self.owner_event2_login_data = {
            "username": 'HaileeSteinfeld',
            "password": '1234',
        }

        self.wrong_artist1_data = {
            "username": 'LadyGaga',
            "password": '1234',
            "is_superuser": False,
            "phone": '23995465422',
            "solo": True,
            "hour_price": 200.0,
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
    def test_fail_to_create_an_artist_when_length_of_phone_is_out_of_range(self):

        artist1 = self.artist1_data.copy()
        artist1['phone'] = '123456789123456789'

        # CREATE AN ARTIST
        response = self.client.post('/api/accounts/', artist1, format='json')
        self.assertEqual(response.status_code, 400)

    def test_get_all_and_only_artists(self):
        artist1 = self.client.post('/api/accounts/', self.artist1_data, format='json')
        self.assertEqual(artist1.status_code, 201)


        artist2 = self.client.post('/api/accounts/', self.artist2_data, format='json')
        self.assertEqual(artist2.status_code, 201)


        owner = self.client.post('/api/accounts/', self.owner_event1_data, format='json')
        self.assertEqual(owner.status_code, 201)

        artists = self.client.get('/api/accounts/artists/', format='json')

        self.assertEqual(len(artists.json()), 2)
        self.assertEqual(artists.status_code, 200)

    def test_get_all_and_only_owners(self):
        artist1 = self.client.post('/api/accounts/', self.artist1_data, format='json')
        self.assertEqual(artist1.status_code, 201)

        owner1 = self.client.post('/api/accounts/', self.owner_event1_data, format='json')
        self.assertEqual(owner1.status_code, 201)

        owner2 = self.client.post('/api/accounts/', self.owner_event2_data, format='json')
        self.assertEqual(owner2.status_code, 201)


        owners = self.client.get('/api/accounts/owners/', format='json')

        self.assertEqual(len(owners.json()), 2)
        self.assertEqual(owners.status_code, 200)


    def test_update_account(self):
        artist = self.client.post('/api/accounts/', self.artist1_data, format='json')
        self.assertEqual(artist.status_code, 201)

        token = self.client.post('/api/login/', self.artist1_login_data, format='json').json()['token']

        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token)

        response = self.client.put('/api/accounts/1/', {'username': 'TaylorSwift'}, format='json')
        self.assertEqual(response.status_code, 200)


        expected_data = self.artist1_data.copy()
        expected_data['username'] = 'TaylorSwift'
        expected_data.pop('password')

        self.assertEqual(response.json(),
                            {
                                'id': 1,
                                **expected_data
                            }
                         )


    def test_fail_to_update_account_of_another_user(self):
        # CREATE AN ARTIST
        artist1 = self.client.post('/api/accounts/', self.artist1_data, format='json')
        self.assertEqual(artist1.status_code, 201)

        # CREATE ANOTHER ARTIST
        artist2 = self.client.post('/api/accounts/', self.artist2_data, format='json')
        self.assertEqual(artist2.status_code, 201)

        # LOGIN AS ARTIST 1
        token = self.client.post('/api/login/', self.artist1_login_data, format='json').json()['token']

        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token)

        # UPDATE ARTIST 2 PROFILE
        response = self.client.put('/api/accounts/2/', {'username': 'TaylorSwift'}, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"detail": "You do not have permission to perform this action."})

    def test_fail_to_update_account_because_token_is_invalid(self):
        # CREATE AN ARTIST
        self.client.post('/api/accounts/', self.artist1_data, format='json')

        # SET CREDENTIALS WITH INVALID TOKEN
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + 'token')

        # UPDATE THE ACCOUNT
        response = self.client.put('/api/accounts/1/', {'username': 'aaa'}, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Invalid token."})

    def test_fail_to_update_account_because_user_not_provide_token(self):
        # CREATE AN ARTIST
        self.client.post('/api/accounts/', self.artist1_data, format='json')

        # CREATE AN OWNER
        self.client.post('/api/accounts/', self.owner_event1_data, format='json')

        # UPDATE ACCOUNT OF THE ARTIST
        response = self.client.put('/api/accounts/1/', {'username': 'aaa'}, format='json')
        self.assertEqual(response.status_code, 401)

        # UPDATE ACCOUNT OF THE OWNER
        response = self.client.put('/api/accounts/2/', {'username': 'bbb'}, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})

    def test_fail_to_update_an_account_because_id_not_found(self):
        self.client.post('/api/accounts/', self.artist2_data, format='json')
        token = self.client.post('/api/login/', self.artist2_login_data, format='json').json()['token']
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token)

        response = self.client.put('/api/accounts/10/', {'username': 'TaylorSwift'}, format='json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'error': 'User not founded.'})

    def test_fail_to_update_is_superuser_field(self):
        # CREATE AN ARTIST AND LOGIN AS HER
        self.client.post('/api/accounts/', self.artist1_data, format='json')
        token = self.client.post('/api/login/', self.artist1_login_data, format='json').json()['token']
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token)

        # UPDATE IS_SUPERUSER FIELD
        response = self.client.put('/api/accounts/1/', {'is_superuser': True}, format='json')
        self.assertEqual(response.status_code, 400)

        # CREATE AN OWNER AND LOGI AS HER
        self.client.post('/api/accounts/', self.owner_event1_data, format='json')
        token = self.client.post('/api/login/', self.owner_event1_login_data, format='json').json()['token']
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token)

        # UPDATE IS_SUPERUSER FIELD
        response = self.client.put('/api/accounts/2/', {'is_superuser': False}, format='json')

        self.assertEqual(response.status_code, 400)

    def test_delete_account(self):
        owner = self.client.post('/api/accounts/', self.owner_event2_data, format='json')
        self.assertEqual(owner.status_code, 201)

        token = self.client.post('/api/login/', self.owner_event2_login_data, format='json').json()['token']

        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token)
        response = self.client.delete('/api/accounts/1/')


        self.assertEqual(response.status_code, 204)

    def test_fail_to_delete_account_because_token_is_invalid(self):
        # CREATE AN OWNER
        self.client.post('/api/accounts/', self.owner_event1_data, format='json')

        # SET CREDENTIALS WITH INVALID TOKEN
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + 'token')

        # UPDATE THE ACCOUNT
        response = self.client.put('/api/accounts/1/', {'username': 'aaa'}, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Invalid token."})

    def test_fail_to_delete_an_account_of_another_user(self):
        # CREATE AN OWNER
        owner = self.client.post('/api/accounts/', self.owner_event2_data, format='json')
        self.assertEqual(owner.status_code, 201)

        # CREATE AN ARTIST
        artist = self.client.post('/api/accounts/', self.artist2_data, format='json')
        self.assertEqual(artist.status_code, 201)

        # LOGIN AS OWNER
        token = self.client.post('/api/login/', self.owner_event2_login_data, format='json').json()['token']

        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token)

        # DELETE ARTIST ACCOUNT
        response = self.client.delete('/api/accounts/2/')
        self.assertEqual(response.status_code, 403)

    def test_fail_to_delete_a_account_which_id_not_found(self):

        self.client.post('/api/accounts/', self.artist1_data, format='json')
        token = self.client.post('/api/login/', self.artist1_login_data, format='json').json()['token']
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + token)

        response = self.client.delete('/api/accounts/10/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'error': 'User not founded.'})
