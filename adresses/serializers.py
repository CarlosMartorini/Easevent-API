from rest_framework import serializers

from adresses.models import AdressesModel


class AdressesSerializer(serializers.Serializer):
    class Meta:
        model = AdressesModel
        fields = '__all__'
