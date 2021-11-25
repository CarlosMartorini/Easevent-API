from django.db import models


class AdressesModel(models.Model):
    street = models.CharField(max_length=255, null=False)
    neighbourhood = models.CharField(max_length=255,null=False)
    number = models.IntegerField()
    city = models.CharField(max_length=255,null=False)
    state = models.CharField(max_length=255,null=False)

