from django.conf.urls import url, include


urlpatterns = [
    url(r'^event/', include('event.urls.apis', namespace='event')),
    url(r'^member/', include('member.urls.apis', namespace='member')),
]

