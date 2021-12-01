from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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

    def list(self, *args, **kwargs):
        queryset = FeedbackModel.objects\
                                .all()\
                                .filter(event_id=self.kwargs['event_id'])

        serializer = FeedbackSerializer(queryset, many = True,
            fields=['id', 'description', 'stars', 'event'])

        return Response(serializer.data)


