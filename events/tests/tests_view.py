from django.test import TestCase
from django.utils import timezone
from events.models import EventModel
from events.serializers import EventLineupCandidaturesSerializer
from music_styles.models import MusicStyleModel
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from users.models import User


class TestEventViews(TestCase):

    def setUp(self) -> None:
        self.base_url = "/api/events/"
        self.datetime = timezone.now()
        self.repeat_event = 'Weekly'
        self.details = 'details'
        self.base_price = 9.99
        self.client = APIClient()

        self.owner = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='123',
            is_superuser=True
        )

        self.artist_data = {
            'username': 'artist',
            'email': 'artist@example.com',
            'password': '123',
            'is_superuser': False,
            'phone': '70707070',
            'solo': True,
            'hour_price': 9.99
        }

        self.artist_login = {
            'username': 'artist',
            'password': '123'
        }

        self.address = {
            'street': 'E 39th St',
            'neighbourhood': 'Murray Hill',
            'number': 39,
            'city': 'New York',
            'state': 'NY',
            'country': 'New York',
        }

        self.music_styles = [
            {
                "name": "Rock"
            },
            {
                "name": "Country"
            }
        ]

        self.event_data = {
            'datetime': self.datetime,
            'repeat_event': self.repeat_event,
            'details': self.details,
            'base_price': self.base_price,
            'address': self.address,
            'music_styles': self.music_styles,
        }

        self.token_owner = Token.objects.create(user=self.owner)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_owner.key}')

    def test_create_new_event(self):
        response = self.client.post(f'{self.base_url}', self.event_data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['id'], 1)

    def test_create_new_event_with_missing_fields(self):
        self.event_data.pop('address')
        response = self.client.post(f'{self.base_url}', self.event_data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['address'][0], "This field is required.")

    def test_create_new_event_with_music_style_already_exists(self):
        for music_style in self.music_styles:
            MusicStyleModel.objects.create(**music_style)

        response = self.client.post(f'{self.base_url}', self.event_data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['id'], 1)
        self.assertEqual(len(self.music_styles), MusicStyleModel.objects.count())

    def test_artist_cannot_create_new_event(self):
        artist = self.client.post('/api/accounts/', self.artist_data, format='json')
        token_artist = self.client.post('/api/login/', self.artist_login, format='json').json()['token']

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token_artist}')

        response = self.client.post(f'{self.base_url}', self.event_data, format='json')

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['detail'], "You do not have permission to perform this action.")

    def test_artist_applies_for_the_event(self):
        event = self.client.post(f'{self.base_url}', self.event_data, format='json').json()

        artist = self.client.post('/api/accounts/', self.artist_data, format='json').json()
        token_artist = self.client.post('/api/login/', self.artist_login, format='json').json()['token']

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token_artist}')

        response = self.client.patch(f"{self.base_url}{event['id']}/candidatures/")

        self.assertEqual(response.status_code, 200)

        count_candidatures = EventModel.objects.get(id=event['id']).candidatures.count()
        self.assertEqual(1, count_candidatures)

    def test_artist_applies_for_the_event_with_invalid_id(self):
        artist = self.client.post('/api/accounts/', self.artist_data, format='json').json()
        token_artist = self.client.post('/api/login/', self.artist_login, format='json').json()['token']

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token_artist}')
        invalid_event_id = EventModel.objects.count() + 1
        response = self.client.patch(f"{self.base_url}{invalid_event_id}/candidatures/")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['detail'], "Not found.")
        
    def test_owner_reject_artist_apllies(self):
        event = self.client.post(f'{self.base_url}', self.event_data, format='json').json()

        artist = self.client.post('/api/accounts/', self.artist_data, format='json').json()
        token_artist = self.client.post('/api/login/', self.artist_login, format='json').json()['token']

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token_artist}')

        self.client.patch(f"{self.base_url}{event['id']}/candidatures/")
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_owner.key}')

        remove_artists = {
            "remove_artists": [artist['id']]
        }

        response = self.client.patch(f"{self.base_url}{event['id']}/candidatures/", remove_artists, format='json')
        count_candidatures = EventModel.objects.get(id=event['id']).candidatures.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, count_candidatures)

    def test_insert_artist_in_lineup(self):
        event = self.client.post(f'{self.base_url}', self.event_data, format='json').json()

        artist = self.client.post('/api/accounts/', self.artist_data, format='json').json()
        token_artist = self.client.post('/api/login/', self.artist_login, format='json').json()['token']

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token_artist}')

        self.client.patch(f"{self.base_url}{event['id']}/candidatures/")

        lineup = {
            "lineup": [{
                "artist_id": artist['id'],
                "performance_datetime": "2021-12-2 20:00:00"
            }
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_owner.key}')

        response = self.client.patch(f"{self.base_url}{event['id']}/lineup/", lineup, format='json')
        event = EventModel.objects.get(id=event['id'])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, event.lineup.count())
        self.assertEqual(0, event.candidatures.count())

    def test_insert_artist_no_candidate_in_lineup_event(self):
        event = self.client.post(f'{self.base_url}', self.event_data, format='json').json()

        artist = self.client.post('/api/accounts/', self.artist_data, format='json').json()

        lineup = {
            "lineup": [{
                "artist_id": artist['id'],
                "performance_datetime": "2021-12-2 20:00:00"
            }
            ]
        }

        response = self.client.patch(f"{self.base_url}{event['id']}/lineup/", lineup, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], f"Artist with id {artist['id']} not in candidatures")

    def test_cannot_insert_artist_with_performance_datetime_before_event_datetime(self):
        event = self.client.post(f'{self.base_url}', self.event_data, format='json').json()

        artist = self.client.post('/api/accounts/', self.artist_data, format='json').json()
        lineup = {
            "lineup": [{
                "artist_id": artist['id'],
                "performance_datetime": "2021-12-20 20:00:00"
            }
            ]
        }

        response = self.client.patch(f"{self.base_url}{event['id']}/lineup/", lineup, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], f"Performance datetime day is after event day for artist with id {artist['id']}")

    def test_insert_artist_in_lineup_non_existent_event(self):
        event = self.client.post(f'{self.base_url}', self.event_data, format='json').json()

        artist = self.client.post('/api/accounts/', self.artist_data, format='json').json()
        token_artist = self.client.post('/api/login/', self.artist_login, format='json').json()['token']

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token_artist}')

        self.client.patch(f"{self.base_url}{event['id']}/candidatures/")

        lineup = {
            "lineup": [{
                "artist_id": artist['id'],
                "performance_datetime": "2021-12-2 20:00:00"
            }
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_owner.key}')

        response = self.client.patch(f"{self.base_url}{event['id'] + 1}/lineup/", lineup, format='json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['detail'], "Not found.")

    def test_insert_non_existent_artist_in_lineup_event(self):
        event = self.client.post(f'{self.base_url}', self.event_data, format='json').json()

        artist = self.client.post('/api/accounts/', self.artist_data, format='json').json()
        token_artist = self.client.post('/api/login/', self.artist_login, format='json').json()['token']

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token_artist}')

        self.client.patch(f"{self.base_url}{event['id']}/candidatures/")

        lineup = {
            "lineup": [{
                "artist_id": artist['id'] + 1,
                "performance_datetime": "2021-12-2 20:00:00"
            }
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_owner.key}')

        response = self.client.patch(f"{self.base_url}{event['id']}/lineup/", lineup, format='json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['detail'], "Not found.")

    def test_update_event(self):

        event = self.client.post(f'{self.base_url}', self.event_data, format='json').json()

        self.event_data['details'] = 'details updated'
        self.event_data['base_price'] = 100

        response = self.client.put(f"{self.base_url}{event['id']}/", self.event_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['details'], self.event_data['details'])
        self.assertEqual(response.json()['base_price'],  self.event_data['base_price'])

    def test_list_events(self):
        event = self.client.post(f'{self.base_url}', self.event_data, format='json').json()
        event = EventModel.objects.get(id=event['id'])

        response = self.client.get(self.base_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), EventModel.objects.count())
        self.assertIn(EventLineupCandidaturesSerializer(instance=event).data, response.data)

    def test_get_event_by_id(self):
        event = self.client.post(f'{self.base_url}', self.event_data, format='json').json()

        response = self.client.get(f'{self.base_url}{event["id"]}/')
        event = EventModel.objects.get(id=event['id'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(EventLineupCandidaturesSerializer(instance=event).data, response.data)

    def test_delete_event(self):
        event = self.client.post(f'{self.base_url}', self.event_data, format='json').json()
        response = self.client.delete(f'{self.base_url}{event["id"]}/')

        self.assertEqual(response.status_code, 204)

    def test_delete_non_existent_event(self):
        invalid_event_id = EventModel.objects.count() + 1
        response = self.client.delete(f'{self.base_url}{invalid_event_id}/')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['detail'], "Not found.")
