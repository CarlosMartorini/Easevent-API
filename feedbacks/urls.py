from rest_framework.routers import SimpleRouter

from feedbacks.views import FeedbackViews

router = SimpleRouter()
router.register('feedbacks', FeedbackViews)
urlpatterns = router.urls