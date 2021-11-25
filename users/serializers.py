from rest_framework import serializers
from users.models import User

class DynamicFieldsModelUserSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):

        fields = kwargs.pop('fields', None)

        super(DynamicFieldsModelUserSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class UserSerializer(DynamicFieldsModelUserSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'is_superuser', 'phone', 'solo', 'hour_price',)
