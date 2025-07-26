# chats/filters.py

import django_filters
from .models import Message  # Adjust path as needed
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageFilter(django_filters.FilterSet):
    sender = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    receiver = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    created_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'created_at']

