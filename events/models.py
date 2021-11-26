from django.db import models


class RepeatEvent(models.TextChoices):
    WEEKLY = 'W', 'Weekly'
    MONTHLY = 'M', 'Monthly'
    NULL = 'N', 'None'


class EventModel(models.Model):
    datetime = models.DateTimeField()
    repeat_event = models.CharField(max_length=1, choices=RepeatEvent.choices, default=RepeatEvent.NULL)
    address = models.ForeignKey('adresses.AdressesModel', on_delete=models.PROTECT)
    owner = models.ForeignKey('users.User', on_delete=models.PROTECT)
    details = models.TextField()
    base_price = models.FloatField()
    lineup = models.ManyToManyField('users.User', related_name='events')
    candidatures = models.ManyToManyField('users.User', related_name='candidatures')
    music_styles = models.ManyToManyField('music_styles.MusicStyleModel')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save()
