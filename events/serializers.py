from rest_framework import serializers

from users.serializers import UserSerializer
from .models import EventModel


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventModel
        fields = '__all__'
        depth = 1


class EventToFeedbacksSerializer(serializers.ModelSerializer):
    owner = UserSerializer(fields=['id', 'username', 'email'])

    class Meta:
        model = EventModel
        exclude = ('candidatures', 'lineup')
        depth = 1