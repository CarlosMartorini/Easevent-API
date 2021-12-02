from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.shortcuts import get_object_or_404
from events.models import EventModel


class IsOwnerOrIfUserReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS and request.user.username:
            return True

        return request.user.is_superuser


class IsOwnerResourceOrCreateRead(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.method == "POST":
            return True

        event = get_object_or_404(EventModel, id=view.kwargs['pk'])

        return request.user.id == event.owner.id
