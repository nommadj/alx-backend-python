from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [DjangoFilterBackend]

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend]

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get("conversation")
        if not conversation_id:
            return Response({"error": "Conversation ID required"}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

