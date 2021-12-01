from datetime import datetime

from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User

from events.models import EventModel
from events.permissions import (IsOwnerOrIfUserReadOnly,
                                IsOwnerResourceOrCreateRead)
from events.serializers import (EventLineupCandidaturesSerializer,
                                EventSerializer)


class EventView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrIfUserReadOnly, IsOwnerResourceOrCreateRead]
    queryset = EventModel.objects.all()
    serializer_class = EventSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET' and self.request.user.is_superuser:
            return EventLineupCandidaturesSerializer
        return super().get_serializer_class()

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        user = self.request.user
        if user.is_superuser:
            queryset = queryset.filter(owner=user)
        else:
            queryset = queryset.filter(datetime__gte=timezone.now())
        return queryset

    @action(detail=True, methods=['patch'])
    def lineup(self, request, pk):
        event = get_object_or_404(EventModel, id=int(pk))

        for artist_data in request.data['lineup']:
            artist = get_object_or_404(User, id=artist_data['artist_id'])
            artist_performance_day = datetime.strptime(artist_data['performance_datetime'], '%Y-%m-%d %H:%M:%S').day

            if event.datetime.day >= artist_performance_day:
                if artist in event.candidatures.all():
                    event.lineup.add(artist, through_defaults={'performance_datetime': artist_data['performance_datetime']})
                    event.candidatures.remove(artist)
                else:
                    return Response({
                        'error': f'Artist with id {artist.id} not in candidatures'
                        }, status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'error': f"Performance datetime day is after event day for artist with id {artist_data['artist_id']}"
                    }, status.HTTP_400_BAD_REQUEST)

        serialized = EventLineupCandidaturesSerializer(event)
        return Response(serialized.data)


class EventCandidatureView(APIView):
    authentication_classes = [TokenAuthentication]

    def patch(self, request, *args, **kwargs):
        event = get_object_or_404(EventModel, id=kwargs.get('pk'))
        if request.user.is_superuser:
            for artist_id in request.data['remove_artists']:
                artist = get_object_or_404(User, id=artist_id)
                event.candidatures.remove(artist)

            serialized = EventLineupCandidaturesSerializer(event)
            return Response(serialized.data)

        artist = get_object_or_404(User, id=request.user.id)
        event.candidatures.add(artist)
        return Response({'msg': 'Application made successfully'})
