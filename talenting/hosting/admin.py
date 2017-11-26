from django.contrib import admin

from hosting.models import Hosting, Photo, Description, HostingReview, GeoLocation

admin.site.register(Hosting)
admin.site.register(Photo)
admin.site.register(Description)
admin.site.register(HostingReview)
admin.site.register(GeoLocation)