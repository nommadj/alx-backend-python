from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing users.
    Only allows authenticated users to list and retrieve themselves or other users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    # Optionally, restrict users to only view their own profile or allow admins to view all
    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(user_id=self.request.user.user_id)


class ConversationViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing conversations.
    Users can only see/manage conversations they are a part of.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter conversations to only show those where the requesting user is a participant.
        """
        user = self.request.user
        return Conversation.objects.filter(participants=user).distinct()

    def perform_create(self, serializer):
        """
        When creating a conversation, ensure the current user is a participant.
        The `create` method in the serializer handles adding other participants.
        """
        # We need to modify the request data to include the current user as a participant
        # since the 'participants' field is read_only in the serializer.
        request_data = self.request.data.copy()
        current_user_id = str(self.request.user.user_id)

        if 'participant_ids' not in request_data:
            request_data['participant_ids'] = []

        if current_user_id not in request_data['participant_ids']:
            request_data['participant_ids'].append(current_user_id)

        # Pass the modified request data to the serializer's create method via context
        serializer.context['request'] = self.request
        serializer.context['request'].data.update(request_data) # Update original request data for serializer validation

        serializer.is_valid(raise_exception=True)
        self.object = serializer.save()


    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """
        Custom action to send a message within a specific conversation.
        """
        conversation = self.get_object() # Ensures the user has access to this conversation

        # Check if the requesting user is a participant of this conversation
        if not conversation.participants.filter(user_id=request.user.user_id).exists():
            return Response(
                {"detail": "You are not a participant of this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            # Automatically set the sender and conversation
            serializer.save(sender=request.user, conversation=conversation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and creating messages.
    Users can only see messages in conversations they are a part of.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter messages to only show those belonging to conversations
        where the requesting user is a participant.
        """
        user = self.request.user
        return Message.objects.filter(
            conversation__participants=user
        ).distinct().order_by('sent_at')

    def perform_create(self, serializer):
        """
        When creating a message, ensure the sender is the current user
        and they are a participant of the target conversation.
        """
        conversation_id = self.request.data.get('conversation')
        if not conversation_id:
            return Response(
                {"conversation": "This field is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {"conversation": "Conversation not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Ensure the current user is a participant of the conversation they are sending a message to
        if not conversation.participants.filter(user_id=self.request.user.user_id).exists():
            return Response(
                {"detail": "You are not a participant of this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer.save(sender=self.request.user, conversation=conversation)
