from django.contrib import admin

from .models.hosting import Hosting, Photo,HostingReview

admin.site.register(Hosting)
admin.site.register(Photo)
admin.site.register(HostingReview)