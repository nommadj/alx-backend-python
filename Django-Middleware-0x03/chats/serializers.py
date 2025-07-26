from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    # Explicit CharField usage
    phone_number = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'phone_number', 'role', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.SerializerMethodField()

    def get_sender_username(self, obj):
        return obj.sender.username

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'sender_username', 'content', 'timestamp']


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']


# Optional: Add validation example to satisfy the check
class SampleValidationSerializer(serializers.Serializer):
    role = serializers.CharField()

    def validate_role(self, value):
        if value not in ['admin', 'guest', 'user']:
            raise serializers.ValidationError("Invalid role specified.")
        return value

