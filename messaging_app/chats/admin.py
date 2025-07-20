from django.contrib import admin\nfrom .models import User, Conversation, Message\n\nadmin.site.register(User)\nadmin.site.register(Conversation)\nadmin.site.register(Message)
