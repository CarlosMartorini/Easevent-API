from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from events.models import EventModel
from music_styles.models import MusicStyleModel
from rest_framework.authtoken.models import Token
from users.models import User


class TestEventViews(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.base_url = "/api/events/"
        cls.datetime = timezone.now()
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
            'address': cls.address,
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
                "performance_datetime": timezone.now() + timedelta(hours=+1)
            }
        ]

        response = self.client.put(f'{self.base_url}/{event.id}', lineup)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['lineup'], lineup)

    def test_cannot_insert_artist_with_performance_datetime_before_event_datetime(self):
        event = self.client.post(f'{self.base_url}', self.event_data)

        artist = self.client.post('/api/accounts/', self.artist_data)
        lineup = [
            {
                "artist_id": artist.id,
                "performance_datetime": timezone.now() - timedelta(hours=+1)
            }
        ]

        response = self.client.put(f'{self.base_url}/{event.id}', lineup)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'performance_datetime should be after event datetime')

    def test_only_artist_can_insert_in_lineup_event(self):
        event = self.client.post(f'{self.base_url}', self.event_data)
        self.artist_data['is_superuser'] = True

        artist = self.client.post('/api/accounts/', self.artist_data)
        lineup = [
            {
                "artist_id": artist.id,
                "performance_datetime": timezone.now() + timedelta(hours=+1)
            }
        ]

        response = self.client.put(f'{self.base_url}/{event.id}', lineup)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], "Only artists can be enrolled in the lineups events.")

    def test_insert_artist_in_lineup_non_existent_event(self):

        artist = self.client.post('/api/accounts/', self.artist_data)
        lineup = [
            {
                "artist_id": artist.id,
                "performance_datetime": timezone.now() + timedelta(hours=+1)
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
                "performance_datetime": timezone.now() + timedelta(hours=+1)
            }
        ]

        response = self.client.put(f'{self.base_url}/{event.id}', lineup)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], "Event not founded!")

    def test_update_event(self):
        event_data_update = {
            'datetime': timezone.now(),
            'base_price': 99.9
        }

        event = self.client.post(f'{self.base_url}', self.event_data)

        response = self.client.put(f'{self.base_url}/{event.id}', event_data_update)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['datetime'], event_data_update['datetime'])
        self.assertEqual(response.json()['base_price'], event_data_update['base_price'])

    def test_list_events(self):
        self.client.post(f'{self.base_url}', self.event_data)

        response = self.client.get(self.base_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0], self.event_data)
        self.assertEqual(len(response.json()), EventModel.objects.count())

    def test_get_event_by_id(self):
        event = self.client.post(f'{self.base_url}', self.event_data)
        response = self.client.get(f'{self.base_url}/{event.id}')

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.event_data, response.json())

    def test_delete_event(self):
        event = self.client.post(f'{self.base_url}', self.event_data)
        response = self.client.delete(f'{self.base_url}/{event.id}')

        self.assertEqual(response.status_code, 204)

    def test_delete_non_existent_event(self):
        invalid_event_id = EventModel.objects.count() + 1
        response = self.client.delete(f'{self.base_url}/{invalid_event_id}')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], "Event not founded.")

    def test_artist_applies_for_event(self):
        event = self.client.post(f'{self.base_url}', self.event_data)
        artist = self.client.post('/api/accounts/', self.artist_data)

        token_artist = Token.objects.create(artist=artist)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token_artist.key}')
        response = self.client.put(f'{self.base_url}/{event.id}/candidatures')

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.artist_data, response.json()['candidatures'])

    def test_artist_applies_for_invalid_id_event(self):
        artist = self.client.post('/api/accounts/', self.artist_data)
        invalid_event_id = EventModel.objects.count() + 1

        token_artist = Token.objects.create(artist=artist)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token_artist.key}')
        response = self.client.put(f'{self.base_url}/{invalid_event_id}/candidatures')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], "Event not founded!")

    def test_owner_accepts_artists_application(self):

        event = self.client.post(f'{self.base_url}', self.event_data)
        artist = self.client.post('/api/accounts/', self.artist_data)

        token_artist = Token.objects.create(artist=artist)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token_artist.key}')
        self.client.put(f'{self.base_url}/{event.id}/candidatures')

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_owner.key}')
        response = self.client.put(f'{self.base_url}/{event.id}/candidatures', {'artist_id': artist.id})

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.artist_data, response.json()['candidatures'])
        self.assertIn(self.artist_data, response.json()['lineup'])

    def test_owner_accepts_artists_application_invalid_id_event(self):

        event = self.client.post(f'{self.base_url}', self.event_data)
        artist = self.client.post('/api/accounts/', self.artist_data)
        invalid_event_id = EventModel.objects.count() + 1

        token_artist = Token.objects.create(artist=artist)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token_artist.key}')
        self.client.put(f'{self.base_url}/{event.id}/candidatures')

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_owner.key}')
        response = self.client.put(f'{self.base_url}/{invalid_event_id}/candidatures', {'artist_id': artist.id})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], "Event not founded!")
