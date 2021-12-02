from django.urls import path
from feedbacks.views import FeedbackViews, get_feedbacks

urlpatterns = [
    path('feedbacks/', get_feedbacks),
    path('events/<int:event_id>/feedbacks/',
         FeedbackViews.as_view({'get': 'list', 'post': 'create'}))
]
