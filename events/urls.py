from django.urls import path
from .views import EventView, EventCandidatureView

from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(prefix=r'events', viewset=EventView)

urlpatterns = [
	path('events/<int:pk>/candidatures/', EventCandidatureView.as_view()),
]
urlpatterns += router.urls
