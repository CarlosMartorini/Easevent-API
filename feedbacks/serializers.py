from rest_framework import serializers
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

class FeedbackDetailsSerializer(DynamicFieldsModelFeedbackSerializer):
    class Meta:
        model = FeedbackModel
        fields = '__all__'
        depth = 1
