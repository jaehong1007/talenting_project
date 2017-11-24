from django.conf.urls import url, include

from member.apis import SignUp

urlpatterns = [
    url(r'^event/', include('event.urls.apis', namespace='event')),
    url(r'^member/signup/$', SignUp.as_view, name='signup'),
    ]

