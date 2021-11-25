from rest_framework import serializers

from adresses.models import AdressesModel


class AdressesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdressesModel
        fields = '__all__'
