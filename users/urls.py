from django.urls import path

from users.views import create_user, login

urlpatterns = [
    path('accounts/', create_user),
    path('login/', login),
]