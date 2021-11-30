from django.test import TestCase
from adresses.models import AdressesModel

from feedbacks.models import FeedbackModel
from users.models import User
from events.models import EventModel
from music_styles.models import MusicStyleModel


class FeedbacksModelTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.username = 'LadyGaga'
        cls.password = '1234'
        cls.email = 'ladygaga@gmail.com'
        cls.is_superuser = False
        cls.phone = '23995465422'
        cls.solo = True
        cls.hour_price = 200.0


        cls.user = User.objects.create(
            username=cls.username,
            password=cls.password,
            email=cls.email,
            is_superuser=cls.is_superuser,
            phone=cls.phone,
            solo=cls.solo,
            hour_price=cls.hour_price
        )

        cls.addressed_username = 'JohnDoe'
        cls.addressed_password = '5678'
        cls.addressed_email = 'john.doe@gmail.com'
        cls.addressed_is_superuser = True

        cls.addressed_user = User.objects.create(
            username=cls.addressed_username,
            password=cls.addressed_password,
            email=cls.addressed_email,
            is_superuser=cls.addressed_is_superuser,
        )

        cls.street = "W Pine St"
        cls.neighbourhood = "Downtown Orlando"
        cls.number = 37
        cls.city = "Orlando"
        cls.state = "Florida"

        cls.address = AdressesModel.objects.create(
            street = cls.street,
            neighbourhood = cls.neighbourhood,
            number = cls.number,
            city = cls.city,
            state = cls.state
        )

        cls.music_style_name = 'Rock'

        cls.music_style = MusicStyleModel.objects.create(
            name = cls.music_style_name
        )

        cls.datetime = '2021-12-10 19:00:00'
        cls.repeat_event = 'None'
        cls.details = 'Some details for local event'
        cls.base_price = 120

        cls.event = EventModel.objects.create(
            datetime = cls.datetime,
            repeat_event = cls.repeat_event,
            address = cls.address,
            owner = cls.addressed_user,
            details = cls.details,
            base_price = cls.base_price,
            music_style = cls.music_style
        )

        cls.description = 'Some description feedback',
        cls.stars = 3

        cls.feedback = FeedbackModel.objects.create(
            from_user = cls.user,
            description = cls.description,
            stars = cls.stars,
            event = cls.event,
            addressed_user = cls.addressed_user
        )

    def test_feedback_model(self):
        self.assertIsInstance(self.feedback.description, str)
        self.assertEqual(self.feedback.description, self.description)

        self.assertIsInstance(self.feedback.stars, int)
        self.assertEqual(self.feedback.stars, self.stars)
