from django.conf.urls import url

from ..apis import EventList, EventDetail

urlpatterns = [
    url(r'^', EventList.as_view(), name='event-list'),
    url(r'^(?P<pk>\d+)/$', EventDetail.as_view(), name='event-detail'),

]