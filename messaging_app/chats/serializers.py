from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the Custom User model.
    Excludes sensitive fields like password.
    """
    class Meta:
        model = User
        fields = (
            'user_id', 'first_name', 'last_name', 'email', 'phone_number',
            'role', 'created_at'
        )
        read_only_fields = ('user_id', 'created_at')

class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.
    Includes sender information nested.
    """
    sender_details = UserSerializer(source='sender', read_only=True) # Nested serializer for sender

    class Meta:
        model = Message
        fields = (
            'message_id', 'conversation', 'sender', 'sender_details',
            'message_body', 'sent_at'
        )
        read_only_fields = ('message_id', 'sent_at', 'sender_details')
        extra_kwargs = {'sender': {'write_only': True}} # Make sender write-only for creation

class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model.
    Includes nested messages and participants.
    """
    participants = UserSerializer(many=True, read_only=True) # Nested serializer for participants
    messages = MessageSerializer(many=True, read_only=True) # Nested serializer for messages

    class Meta:
        model = Conversation
        fields = (
            'conversation_id', 'participants', 'messages', 'created_at'
        )
        read_only_fields = ('conversation_id', 'created_at')

    def create(self, validated_data):
        """
        Handle creation of a conversation with participants.
        Expects 'participant_ids' in initial_data if creating a new conversation.
        """
        # We need to get participant_ids from the request's initial_data
        # since participants is a ManyToManyField and read-only on the serializer
        participant_ids = self.context.get('request').data.get('participant_ids', [])
        if not participant_ids:
            raise serializers.ValidationError({"participant_ids": "At least one participant ID is required to create a conversation."})

        conversation = Conversation.objects.create(**validated_data)
        # Add participants to the conversation
        users = User.objects.filter(user_id__in=participant_ids)
        if not users.exists():
            raise serializers.ValidationError({"participant_ids": "No valid participants found for the provided IDs."})
        conversation.participants.set(users) # Use .set() for ManyToManyField
        return conversation
