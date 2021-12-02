from django.db import models


class FeedbackModel(models.Model):
    from_user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='feedbacks_sent')
    description = models.TextField()
    stars = models.IntegerField(null=False)
    event = models.ForeignKey('events.EventModel', null=False, on_delete=models.CASCADE)
    addressed_user = models.ForeignKey('users.User', null=False, on_delete=models.CASCADE, related_name='feedbacks_received')

