from django.contrib import admin

from .models import Event, EventComment

admin.site.register(Event)
admin.site.register(EventComment)
