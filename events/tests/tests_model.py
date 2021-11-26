from django.test import TestCase
from datetime import datetime, timedelta
from users.models import User
from adresses.models import AdressesModel
from music_styles.models import MusicStyleModel
from events.models import EventModel, RepeatEvent


class TestEventModel(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.datetime = datetime.utcnow()
        cls.repeat_event = RepeatEvent.WEEKLY
        cls.details = 'details'
        cls.base_price = 9.99

        cls.owner = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='123',
            is_superuser=True
        )

        cls.street = 'E 39th St'
        cls.neighbourhood = 'Murray Hill'
        cls.number = 39
        cls.city = 'New York'
        cls.state = 'NY'
        cls.country = 'New York'

        cls.address = AdressesModel.objects.create(
            street=cls.street,
            neighbourhood=cls.neighbourhood,
            number=cls.number,
            city=cls.city,
            state=cls.state,
            country=cls.country,
        )

        cls.event = EventModel.objects.create(
            datetime=cls.datetime,
            repeat_event=RepeatEvent.WEEKLY,
            address=cls.address,
            owner=cls.owner,
            details=cls.details,
            base_price=cls.base_price
        )

    def test_event_model(self):
        self.assertIsInstance(self.event.datetime, datetime)
        self.assertEqual(self.event.datetime, self.datetime)

        self.assertIsInstance(self.event.repeat_event, str)
        self.assertEqual(self.event.repeat_event, self.repeat_event)

        self.assertIsInstance(self.event.details, str)
        self.assertEqual(self.event.details, self.details)

        self.assertIsInstance(self.event.base_price, float)
        self.assertEqual(self.event.base_price, self.base_price)

    def test_event_can_be_attached_to_multiple_music_styles(self):
        self.music_style1 = MusicStyleModel.objects.create(
            name="MusicStyle1"
        )

        self.music_style2 = MusicStyleModel.objects.create(
            name="MusicStyle2"
        )

        self.event.music_styles.add(self.music_style1)
        self.event.music_styles.add(self.music_style2)

        self.assertEquals(2, self.event.music_styles.count())

        self.assertIn(self.music_style1, list(self.event.music_styles.all()))
        self.assertIn(self.music_style2, list(self.event.music_styles.all()))

    def test_event_can_be_attached_to_multiple_artists_in_lineup(self):

        self.artist1 = User.objects.create_user(
            username='artist1',
            email='artist1@example.com',
            is_superuser=False,
            phone="970707070",
            solo=True,
            password='123',
            hour_price=9.99
        )

        self.artist2 = User.objects.create_user(
            username='artist2',
            email='artist2@example.com',
            is_superuser=False,
            phone="97070707070",
            solo=True,
            password='123',
            hour_price=9.99
        )

        self.event.lineup.add(self.artist1, through_defaults={'performance_datetime': self.event.datetime})
        self.event.lineup.add(self.artist2, through_defaults={'performance_datetime': self.event.datetime + timedelta(hours=+1)})

        self.assertEquals(2, self.event.lineup.count())

        self.assertIn(self.artist1, list(self.event.lineup.all()))
        self.assertIn(self.artist2, list(self.event.lineup.all()))

    def test_event_can_be_attached_to_multiple_artists_in_candidatures(self):

        self.artist1 = User.objects.create_user(
            username='artist1',
            email='artist1@example.com',
            is_superuser=False,
            phone="970707070",
            solo=True,
            password='123',
            hour_price=9.99
        )

        self.artist2 = User.objects.create_user(
            username='artist2',
            email='artist2@example.com',
            is_superuser=False,
            phone="97070707070",
            solo=True,
            password='123',
            hour_price=9.99
        )

        self.event.candidatures.add(self.artist1)
        self.event.candidatures.add(self.artist2)

        self.assertEquals(2, self.event.candidatures.count())

        self.assertIn(self.artist1, list(self.event.candidatures.all()))
        self.assertIn(self.artist2, list(self.event.candidatures.all()))
