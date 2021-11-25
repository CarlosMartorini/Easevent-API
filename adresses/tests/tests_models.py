from django.test import TestCase

from adresses.models import Address
from users.models import User
from events.models import Event


class TestAdressesModel(TestCase):
    @classmethod
    def setUpClass(cls) -> None:        
        cls.street = 'E 39th St'
        cls.neighbourhood = 'Murray Hill'
        cls.number = 39
        cls.city = 'New York'
        cls.state = 'NY'
        cls.country = 'New York'

        cls.address = Address.objects.create(
            street = cls.street,
            neighbourhood = cls.neighbourhood,
            number = cls.number,
            city = cls.city,
            state = cls.state,
            country = cls.country,
        )

    def test_adresses_model(self):
        self.assertIsInstance(self.address.street, str)
        self.assertEqual(self.address.street, self.street)

        self.assertIsInstance(self.address.neighbourhood, str)
        self.assertEqual(self.address.neighbourhood, self.neighbourhood)

        self.assertIsInstance(self.address.number, int)
        self.assertEqual(self.address.number, self.number)

        self.assertIsInstance(self.address.city, str)
        self.assertEqual(self.address.city, self.city)

        self.assertIsInstance(self.address.state, str)
        self.assertEqual(self.address.state, self.state)

        self.assertIsInstance(self.address.country, str)
        self.assertEqual(self.address.country, self.country)

