from rest_framework import fields, serializers, status
from rest_framework.exceptions import ValidationError
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

        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


    def validate(self, attrs):
        received_attrs = dict(attrs)
        required_fields = ['hour_price', 'phone', 'solo']
        missing_keys = []

        if not received_attrs['is_superuser']:
            for field in required_fields:
                if field not in received_attrs.keys():
                    missing_keys.append(field)

            if missing_keys:
                raise ValidationError({'details': f'some data is missing: {[*missing_keys]}'})

        return super().validate(attrs)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        if not type(self.initial_data['username']) is str or\
           not type(self.initial_data['password']) is str:
            raise ValidationError({'details': 'incorrect value type of username or password'})

        return super().validate(attrs)