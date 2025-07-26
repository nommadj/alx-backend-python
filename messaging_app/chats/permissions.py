from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Conversation

class IsOwner(permissions.BasePermission):
    """
    Allows access only to objects owned by the requesting user.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user  # Assumes `user` field in model

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to interact with its messages.
    """

    def has_permission(self, request, view):
        # Allow access only to authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Get the related conversation
        conversation = getattr(obj, 'conversation', obj)

        # Check if user is a participant
        is_participant = request.user in conversation.participants.all()

        # Explicitly handle unsafe methods
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return is_participant

        # Allow other methods (e.g., GET, POST) only if user is a participant
        return is_participant
