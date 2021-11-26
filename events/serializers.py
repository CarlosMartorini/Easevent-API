from rest_framework import serializers
from .models import EventModel


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventModel
        fields = '__all__'
        depth = 1