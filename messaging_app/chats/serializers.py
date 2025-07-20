
from rest_framework import serializers
from .models import Message, Conversation, CustomUser

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = '__all__'

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    participants = serializers.SlugRelatedField(many=True, read_only=True, slug_field='username')

    class Meta:
        model = Conversation
        fields = '__all__'

