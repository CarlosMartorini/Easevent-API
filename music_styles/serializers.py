from rest_framework import serializers


class MusicStyleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
