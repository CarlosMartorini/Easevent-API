from rest_framework import  serializers, status
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

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    def validate_empty_values(self, data):

        base_keys = ['username', 'password', 'email', 'is_superuser']
        artist_required_fields = ['hour_price', 'phone', 'solo']
        missing_keys = []

        for field in base_keys:
            if field not in data.keys():
                missing_keys.append(field)

        if not data.get('is_superuser') and\
           not self.instance:

            for field in artist_required_fields:
                if field not in data.keys():
                    missing_keys.append(field)

        if missing_keys:
            raise ValidationError({'required_fields': [*missing_keys]}, code=status.HTTP_406_NOT_ACCEPTABLE)

        return super().validate_empty_values(data)

    def validate(self, attrs):
        received_data = dict(attrs)

        if received_data.get('is_superuser') and self.instance:
           if self.instance.is_superuser != received_data['is_superuser']:

            raise ValidationError({'error': 'is_superuser field cannot change'})

        return super().validate(attrs)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        if not type(self.initial_data['username']) is str or\
           not type(self.initial_data['password']) is str:
            raise ValidationError({'error': 'incorrect value type of username or password'})

        return super().validate(attrs)