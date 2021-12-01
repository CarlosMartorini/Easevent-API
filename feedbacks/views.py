from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from feedbacks.models import FeedbackModel
from feedbacks.serializers import FeedbackSerializer


class FeedbackViews(viewsets.ModelViewSet):
    queryset = FeedbackModel.objects.all()
    serializer_class = FeedbackSerializer
    authentication_classes = [TokenAuthentication]

    def list(self, request, *args, **kwargs):

        if self.request.query_params.get('sent') and not\
           self.request.user.is_authenticated:
               return Response({"detail": "You do not" \
                        "have permission to perform this action."
                    },
                    status=status.HTTP_403_FORBIDDEN)

        return super().list(request, *args, **kwargs)

    def get_serializer(self, *args, **kwargs):

        if self.request.query_params.get('sent'):
            return FeedbackSerializer(
                fields=['id', 'description', 'stars', 'event', 'addressed_user'],
                *args, **kwargs
            )

        return FeedbackSerializer(
            fields=['id', 'description', 'stars', 'event'],
            *args, **kwargs
        )

    def filter_queryset(self, queryset):

        queryset = super().get_queryset()

        if self.request.user.is_authenticated:

            if self.request.query_params.get('sent'):
                queryset = queryset.filter(from_user=self.request.user.id)

            else:
                queryset = queryset.filter(addressed_user=self.request.user.id)

        return super().filter_queryset(queryset)