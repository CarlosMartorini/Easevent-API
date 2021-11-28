from django.urls import path

from users.views import (CreateOrGetAccountsView,
                         RetrieveUpdateOrDeleteAccountView, get_artists,
                         get_owners, login)

urlpatterns = [
    path('accounts/', CreateOrGetAccountsView.as_view()),
    path('accounts/artists/', get_artists),
    path('accounts/owners/', get_owners),
    path('accounts/<int:account_id>/', RetrieveUpdateOrDeleteAccountView.as_view()),
    path('login/', login),
]
