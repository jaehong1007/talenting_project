from django.contrib import admin

from .models.hosting import Hosting, HostingPhoto, HostingReview

admin.site.register(Hosting)
admin.site.register(HostingPhoto)
admin.site.register(HostingReview)