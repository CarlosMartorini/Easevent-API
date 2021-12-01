from events.serializers import EventToFeedbacksSerializer
from rest_framework import serializers
from users.serializers import UserSerializer

from feedbacks.models import FeedbackModel


class DynamicFieldsModelFeedbackSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):

        fields = kwargs.pop('fields', None)

        super(DynamicFieldsModelFeedbackSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class FeedbackSerializer(DynamicFieldsModelFeedbackSerializer):
    from_user = UserSerializer(fields=['id', 'username', 'email'])
    addressed_user = UserSerializer(fields=['id', 'username', 'email'])
    event = EventToFeedbacksSerializer()

    class Meta:
        model = FeedbackModel
        fields = '__all__'
        depth = 2
