from django.contrib import admin

from .models import Event, EventComment, Photo

admin.site.register(Event)
admin.site.register(EventComment)
admin.site.register(Photo)