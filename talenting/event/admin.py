from django.contrib import admin

from .models import Event, EventComment, EventPhoto

admin.site.register(Event)
admin.site.register(EventComment)
admin.site.register(EventPhoto)