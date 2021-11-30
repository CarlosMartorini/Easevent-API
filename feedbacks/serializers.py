from rest_framework import serializers
from feedbacks.models import FeedbackModel


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackModel
        fields = ('description', 'stars', )

class FeedbackDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackModel
        exclude = ['event']
        depth = 1
