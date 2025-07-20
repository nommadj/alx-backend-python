import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'admin') # Set admin role for superuser

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser to include
    additional fields like phone_number and role, and using UUID as PK.
    """
    class Role(models.TextChoices):
        GUEST = 'guest', 'Guest'
        HOST = 'host', 'Host'
        ADMIN = 'admin', 'Admin'

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    # password_hash is handled by Django's built-in password field
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.GUEST, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Use email as the USERNAME_FIELD
    USERNAME_FIELD = 'email'
    # Remove 'username' from REQUIRED_FIELDS if it's there from AbstractUser default
    REQUIRED_FIELDS = ['first_name', 'last_name'] # These fields will be prompted when creating a superuser

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Conversation(models.Model):
    """
    Model to track conversations between users.
    A conversation can have multiple participants (users).
    """
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # List participants' emails for easy identification
        return f"Conversation {self.conversation_id} with participants: {', '.join([p.email for p in self.participants.all()])}"

class Message(models.Model):
    """
    Model to store individual messages within a conversation.
    """
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message_body = models.TextField(null=False, blank=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.email} in Conversation {self.conversation.conversation_id}"

    class Meta:
        ordering = ['sent_at'] # Order messages by time sent
