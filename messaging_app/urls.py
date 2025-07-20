from django.contrib import admin\nfrom django.urls import path, include\n\nurlpatterns = [\n    path('admin/', admin.site.urls),\n    path('api/', include('chats.urls')),\n]
