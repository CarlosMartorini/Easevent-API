from django.db import models


class AdressesModel(models.Model):
    street = models.CharField(null=False)
    neighbourhood = models.CharField(null=False)
    number = models.IntegerField()
    city = models.CharField(null=False)
    state = models.CharField(null=False)

