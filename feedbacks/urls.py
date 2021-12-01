from django.urls import path
from feedbacks.views import FeedbackViews, list_own_feedbacks

urlpatterns = [
    path('feedbacks/', list_own_feedbacks),
    path('events/<int:event_id>/feedbacks/',
         FeedbackViews.as_view({'get': 'list'}))
]
