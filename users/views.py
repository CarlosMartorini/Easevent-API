from rest_framework import status
from rest_framework.authentication import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from users.serializers import LoginSerializer, UserSerializer


@api_view(['post'])
def create_user(request):

    user = request.data

    try:
        if user['is_superuser']:
            serializer = UserSerializer(data=user, fields=['id', 'username', 'email', 'is_superuser', 'password'])

        else:

            serializer = UserSerializer(data=user)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except KeyError as e:
        return Response({'required_fields': [*e.args]}, status=status.HTTP_406_NOT_ACCEPTABLE)

    except ValidationError as e:

        if 'unique' in [code[0] for code in e.get_codes().values()]:
            return Response({'error': 'User already exists!'}, status=status.HTTP_409_CONFLICT)

        if '406' in [code[0] for code in e.get_codes().values()]:
            return Response(e.detail, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['post'])
def login(request):

    try:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)

        if user:
            token = Token.objects.get_or_create(user=user)[0]
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'Username or password may be wrong!'}, status=status.HTTP_401_UNAUTHORIZED)

    except ValidationError as e:
        return Response(e.detail, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
