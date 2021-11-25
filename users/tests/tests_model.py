from django.test import TestCase
from users.models import User

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.username = 'Lady Gaga'
        cls.password = '1234'
        cls.email = 'ladygaga@gmail.com'
        cls.is_superuser = False
        cls.phone = '23995465422'
        cls.solo = True
        cls.hour_price = 200


        cls.user = User.objects.create(
            username=cls.username,
            password=cls.password,
            email=cls.email,
            is_superuser=cls.is_superuser,
            phone=cls.phone,
            solo=cls.solo,
            hour_price=cls.hour_price
        )

    def test_user_fields(self):
        self.assertIsInstance(self.user.username, str)
        self.assertEqual(self.user.username, self.username)

        self.assertIsInstance(self.user.password, str)
        self.assertEqual(self.user.password, self.password)

        self.assertIsInstance(self.user.email, str)
        self.assertEqual(self.user.email, self.email)

        self.assertIsInstance(self.user.is_superuser, bool)
        self.assertEqual(self.user.is_superuser, self.is_superuser)

        self.assertIsInstance(self.user.phone, str)
        self.assertEqual(self.user.phone, self.phone)

        self.assertIsInstance(self.user.solo, bool)
        self.assertEqual(self.user.solo, self.solo)

        self.assertIsInstance(self.user.hour_price, float)
        self.assertEqual(self.user.hour_price, self.hour_price)