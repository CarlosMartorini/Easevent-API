from django.db import models


class EventModel(models.Model):
    datetime = models.DateTimeField()
    repeat_datetime = models.BooleanField(default=False)
    address = models.ForeignKey('adresses.AdressesModel', on_delete=models.PROTECT)
    owner = models.ForeignKey('users.User', on_delete=models.PROTECT)
    details = models.TextField()
    base_price = models.FloatField()
    lineup = models.ManyToManyField('users.User', related_name='events')
    music_styles = models.ManyToManyField('music_styles.MusicStyleModel')
