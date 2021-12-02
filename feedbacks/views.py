from django.db.utils import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404
from events.models import EventModel
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import User

from feedbacks.models import FeedbackModel
from feedbacks.serializers import FeedbackSerializer


@api_view(['get'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_own_feedbacks(request):
    queryset = FeedbackModel.objects.all()

    queryset = queryset.filter(from_user=request.user.id)
    serializer = FeedbackSerializer(queryset, many = True,
            fields=['id', 'description', 'stars', 'event', 'addressed_user'])

    return Response(serializer.data)

class FeedbackViews(viewsets.ViewSet):
    queryset = FeedbackModel.objects.all()
    serializer_class = FeedbackSerializer
    authentication_classes = [TokenAuthentication]

    def list(self, _, event_id: int = ''):
        try:
            get_object_or_404(EventModel, id=event_id)
            queryset = FeedbackModel.objects\
                                    .all()\
                                    .filter(event_id=event_id)

            serializer = FeedbackSerializer(queryset, many = True,
                fields=['id', 'description', 'stars', 'event'])

            return Response(serializer.data)
        except Http404:
            return Response({'error': 'Event not founded!'}, status=status.HTTP_404_NOT_FOUND)


    def create(self, request, event_id: int = ''):

        data = request.data
        current_user = self.request.user

        try:
            found_event = EventModel.objects.get(id=event_id)

            data['from_user'] = current_user

            data['addressed_user'] = User.objects.get(id=data['addressed_user'])

            data['event'] = found_event

            if found_event.owner.id == current_user.id or\
                current_user in found_event.lineup.get_queryset():

                    serializer = FeedbackSerializer(data=request.data)

                    serializer.is_valid(raise_exception=True)
                    serializer.save()

                    return Response(serializer.data, status=status.HTTP_201_CREATED)

            else:
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        except (KeyError, ValidationError):
            return Response({'required_fields': ['description', 'stars', 'addressed_user']}, status=status.HTTP_406_NOT_ACCEPTABLE)

        except User.DoesNotExist:
            return Response({'error': 'User not founded.'}, status=status.HTTP_404_NOT_FOUND)

        except EventModel.DoesNotExist:
            return Response({'error': 'Event not founded!'}, status=status.HTTP_404_NOT_FOUND)

        except IntegrityError as e:
            return Response({'error': str(e)}, status=status.HTTP_409_CONFLICT)
