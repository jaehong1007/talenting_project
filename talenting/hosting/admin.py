from django.contrib import admin

from hosting.models import LocationInfo, Hosting, Photo, Description, HostingReview

admin.site.register(Hosting)
admin.site.register(Photo)
admin.site.register(Description)
admin.site.register(HostingReview)
admin.site.register(LocationInfo)