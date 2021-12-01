from events.serializers import EventToFeedbacksSerializer
from rest_framework import serializers
from users.serializers import UserSerializer
from rest_framework.exceptions import ValidationError
from feedbacks.models import FeedbackModel
from django.db.utils import IntegrityError

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
    from_user = UserSerializer(fields=['id', 'username', 'email'], read_only=True)
    addressed_user = UserSerializer(fields=['id', 'username', 'email'], read_only=True)
    event = EventToFeedbacksSerializer(read_only=True)

    class Meta:
        model = FeedbackModel
        fields = '__all__'
        depth = 2

    def create(self, validated_data):
        from_user = self.initial_data['from_user']
        addressed_user = self.initial_data['addressed_user']
        event = self.initial_data['event']

        return FeedbackModel.objects.get_or_create(**validated_data, from_user=from_user, addressed_user=addressed_user, event=event)[0]

    def validate(self, attrs):

        addressed_user_feedbacks = self.initial_data['addressed_user'].feedbacks_received.get_queryset()

        if self.initial_data['from_user'] in [feedback.from_user for feedback in addressed_user_feedbacks]:
            raise IntegrityError('You already made this feedback')

        if self.initial_data['from_user'].is_superuser == self.initial_data['addressed_user'].is_superuser:
            raise ValidationError({'error': 'You can not make a feedback to the same type of user as you'})
        return super().validate(attrs)