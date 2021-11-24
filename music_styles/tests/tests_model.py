from django.test import TestCase
from music_styles.models import MusicStyle


class TestMusicStyleModel(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.name = 'music_style'
        cls.music_style = MusicStyle.objects.create(name=cls.name)

    def test_music_style_model(self):
        self.assertIsInstance(self.music_style.name, str)
        self.assertEqual(self.music_style.name, self.name)
