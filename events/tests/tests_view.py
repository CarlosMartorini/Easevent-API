from django.test import TestCase
from datetime import datetime, timedelta
from users.models import User
from adresses.models import Address
from music_styles.models import MusicStyleModel
from events.models import EventModel
from rest_framework.authtoken.models import Token


class TestEventViews(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.base_url = "/api/events/"
        cls.datetime = datetime.utcnow()
        cls.repeat_event = 'Weekly'
        cls.details = 'details'
        cls.base_price = 9.99

        cls.owner = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='123',
            is_superuser=True
        )

        cls.artist_data = {
            'username': 'artist',
            'email': 'artist@example.com',
            'password': '123',
            'is_superuser': False,
            'phone': '70707070',
            'solo': True,
            'hour_price': 9.99
        }

        cls.address = {
            'street': 'E 39th St',
            'neighbourhood': 'Murray Hill',
            'number': 39,
            'city': 'New York',
            'state': 'NY',
            'country': 'New York',
        }

        cls.music_styles = [
            {
                "name": "Rock"
            },
            {
                "name": "Country"
            }
        ]

        cls.event_data = {
            'datetime': cls.datetime,
            'repeat_event': cls.repeat_event,
            'details': cls.details,
            'base_price': cls.base_price,
            'addresses': cls.address,
            'music_styles': cls.music_styles,
        }

        cls.token_owner = Token.objects.create(user=cls.owner)

        cls.client.credentials(HTTP_AUTHORIZATION=f'Token {cls.token_owner.key}')

    def test_create_new_event(self):
        response = self.client.post(f'{self.base_url}', self.event_data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['id'], 1)

    def test_create_new_event_with_missing_fields(self):
        self.event_data.pop('address')
        response = self.client.post(f'{self.base_url}', self.event_data)

        self.assertEqual(response.status_code, 406)
        self.assertEqual(response.json()['error'], "Date it's missing")

    def test_create_new_event_with_music_style_already_exists(self):
        for music_style in self.music_styles:
            MusicStyleModel.objects.create(**music_style)

        response = self.client.post(f'{self.base_url}', self.event_data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['id'], 1)
        self.assertEqual(len(self.music_styles), MusicStyleModel.objects.count())

    def test_artist_cannot_create_new_event(self):
        artist = self.client.post('/api/accounts/', self.artist_data)
        token_artist = Token.objects.create(artist=artist)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token_artist.key}')

        response = self.client.post(f'{self.base_url}', self.event_data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['detail'], "You do not have permission to perform this action.")

    def test_insert_artist_in_lineup_event(self):
        event = self.client.post(f'{self.base_url}', self.event_data)

        artist = self.client.post('/api/accounts/', self.artist_data)
        lineup = [
            {
                "artist_id": artist.id,
                "performance_datetime": "2021-12-10 20:00:00"
            }
        ]

        response = self.client.put(f'{self.base_url}/1', lineup)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['lineup'], lineup)

    def test_only_artist_can_insert_in_lineup_event(self):
        event = self.client.post(f'{self.base_url}', self.event_data)
        self.artist_data['is_superuser'] = True

        artist = self.client.post('/api/accounts/', self.artist_data)
        lineup = [
            {
                "artist_id": artist.id,
                "performance_datetime": "2021-12-10 20:00:00"
            }
        ]

        response = self.client.put(f'{self.base_url}/1', lineup)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], "Only artists can be enrolled in the lineups events.")

    def test_insert_artist_in_lineup_non_existent_event(self):

        artist = self.client.post('/api/accounts/', self.artist_data)
        lineup = [
            {
                "artist_id": artist.id,
                "performance_datetime": "2021-12-10 20:00:00"
            }
        ]

        response = self.client.put(f'{self.base_url}/1', lineup)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], "Event not founded!")

    def test_insert_non_existent_artist_in_lineup_event(self):
        event = self.client.post(f'{self.base_url}', self.event_data)

        invalid_id = User.objects.count() + 1
        lineup = [
            {
                "artist_id": invalid_id,
                "performance_datetime": "2021-12-10 20:00:00"
            }
        ]

        response = self.client.put(f'{self.base_url}/1', lineup)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], "Event not founded!")

    def test_update_event(self):
        event_data_update = {
            'datetime': datetime.utcnow(),
            'base_price': 99.9
        }

        event = self.client.post(f'{self.base_url}', self.event_data)

        response = self.client.put(f'{self.base_url}/1', event_data_update)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['datetime'], event_data_update['datetime'])
        self.assertEqual(response.json()['base_price'], event_data_update['base_price'])

    def test_list_events(self):
        event = self.client.post(f'{self.base_url}', self.event_data)

        response = self.client.get(self.base_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0], self.event_data)
        self.assertEqual(len(response.json()), EventModel.objects.count())

    def test_delete_event(self):
        event = self.client.post(f'{self.base_url}', self.event_data)
        response = self.client.delete(f'{self.base_url}/1')

        self.assertEqual(response.status_code, 204)

    def test_delete_non_existent_event(self):
        response = self.client.delete(f'{self.base_url}/1')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], "Event not founded.")
