from django.conf.urls import url, include


urlpatterns = [
    url(r'^event/', include('event.urls.apis', namespace='event')),
    url(r'^hosting/', include('hosting.urls.apis', namespace='hosting')),
    url(r'^member/', include('member.urls.apis', namespace='member')),
    url(r'^fcm/', include('fcm.urls.apis', namespace='fcm')),
]
