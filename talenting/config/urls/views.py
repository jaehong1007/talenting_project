from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    url(r'^admin/', admin.site.urls),
    url(r'^member/', include('member.urls.views', namespace='member')),
]
