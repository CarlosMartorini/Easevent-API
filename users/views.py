from rest_framework import status
from rest_framework.authentication import TokenAuthentication, authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import LoginSerializer, UserSerializer


@api_view(['get'])
def get_owners(_):
        owners = User.objects.filter(is_superuser=True)

        serializer = UserSerializer(owners, fields=['id', 'username', 'email', 'is_superuser', 'password'], many=True)

        return Response(serializer.data)

@api_view(['get'])
def get_artists(_):
        artists = User.objects.filter(is_superuser=False)
        serializer = UserSerializer(artists,many=True)

        return Response(serializer.data)

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

        if 415 in [code[0] for code in e.get_codes().values()]:
                return Response(e.detail, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        if 406 in [code[0] for code in e.get_codes().values()]:
                return Response(e.detail, status=status.HTTP_406_NOT_ACCEPTABLE)

        return Response(e.detail, status=e.status_code)

class CreateOrGetAccountsView(APIView):
    def post(self, request):

        user = request.data

        try:

            if user.get('is_superuser'):
                serializer = UserSerializer(data=user, fields=['id', 'username', 'email', 'is_superuser', 'password'])

            else:
                serializer = UserSerializer(data=user)

            serializer.is_valid(raise_exception=True)

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:

            if 'unique' in [code[0] for code in e.get_codes().values()]:
                return Response({'error': 'User already exists!'}, status=status.HTTP_409_CONFLICT)

            if 406 in [code[0] for code in e.get_codes().values()]:
                return Response(e.detail, status=status.HTTP_406_NOT_ACCEPTABLE)

            return Response(e.detail, status=e.status_code)

class RetrieveUpdateOrDeleteAccountView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, account_id: int = ''):

        data = request.data

        try:
            instance = User.objects.get(id=account_id)

            if  self.request.user.id != instance.id:
                return Response({"detail": "You do not have permission to perform this action."},
                                status=status.HTTP_403_FORBIDDEN)

            if instance.is_superuser:
                serializer = UserSerializer(instance, data, fields=['id', 'username', 'email', 'is_superuser', 'password'], partial=True)

            else:
                serializer = UserSerializer(instance, data, partial=True)

            serializer.is_valid(raise_exception=True)

            serializer.save()

            return Response(serializer.data)

        except User.DoesNotExist:
            return Response({"error": "User not founded."},
                            status=status.HTTP_404_NOT_FOUND)

        except ValidationError as e:
            return Response(e.detail, status=e.status_code)

    def get(self, _, account_id: int = ''):
        instance = User.objects.get(id=account_id)

        if instance.is_superuser:
            serializer = UserSerializer(instance, fields=['id', 'username', 'email', 'is_superuser', 'password'])

        else:
            serializer = UserSerializer(instance)

        return Response(serializer.data)

    def delete(self, _, account_id: int = ''):
        try:
            instance = User.objects.get(id=account_id)

            if self.request.user.id == instance.id:
                instance.delete()

                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"detail": "You do not have permission to perform this action."},
                                status=status.HTTP_403_FORBIDDEN)

        except User.DoesNotExist:
            return Response({"error": "User not founded."},
                            status=status.HTTP_404_NOT_FOUND)
