from adresses.models import AdressesModel
from adresses.serializers import AdressesSerializer
from django.shortcuts import get_object_or_404
from music_styles.models import MusicStyleModel
from rest_framework import serializers
from users.models import User
from users.serializers import UserSerializer

from .models import EventModel, LineupEventModel


class MusicStyleSerializerWithoutId(serializers.Serializer):
    name = serializers.CharField()


class EventSerializer(serializers.ModelSerializer):
    address = AdressesSerializer()
    music_styles = MusicStyleSerializerWithoutId(many=True)

    class Meta:
        model = EventModel
        exclude = ['lineup', 'candidatures', 'owner']

    def create(self, validated_data):

        music_styles = validated_data.pop('music_styles')
        address_data = validated_data.pop('address')
        address, _ = AdressesModel.objects.get_or_create(**address_data)
        owner = get_object_or_404(User, id=self.context['request'].user.id)
        validated_data['owner'] = owner
        validated_data['address'] = address
        event = EventModel.objects.create(**validated_data)

        for music_style in music_styles:
            event_music_style, _ = MusicStyleModel.objects.get_or_create(**music_style)
            event.music_styles.add(event_music_style)

        return event

    def update(self, instance, validated_data):

        address_data = validated_data.pop('address')
        address, _ = AdressesModel.objects.get_or_create(**address_data)
        music_styles = validated_data.pop('music_styles')
        instance.music_styles.clear()
        validated_data['address'] = address

        for music_style in music_styles:
            event_music_style, _ = MusicStyleModel.objects.get_or_create(**music_style)
            instance.music_styles.add(event_music_style)

        return super().update(instance, validated_data)


class LineupEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineupEventModel
        fields = ['artist', 'performance_datetime']


class EventLineupCandidaturesSerializer(serializers.ModelSerializer):
    address = AdressesSerializer()
    music_styles = MusicStyleSerializerWithoutId(many=True)
    lineup = LineupEventSerializer(many=True, source='lineup_set')
    candidatures = UserSerializer(fields=['username', 'id', 'phone', 'solo', 'hour_price'], many=True)

    class Meta:
        model = EventModel
        exclude = ['owner']

class EventToFeedbacksSerializer(serializers.ModelSerializer):
    owner = UserSerializer(fields=['id', 'username', 'email'])

    class Meta:
        model = EventModel
        exclude = ('candidatures', 'lineup')
        depth = 1
