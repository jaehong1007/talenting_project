from django.conf.urls import url

from ..apis import EventList, EventDetail, EventParticipateToggle

urlpatterns = [
    url(r'^$', EventList.as_view(), name='event-list'),
    url(r'^(?P<event_pk>\d+)/$', EventDetail.as_view(), name='event-detail'),
    url(r'^(?P<event_pk>\d+)/participate/$', EventParticipateToggle.as_view(), name='event-participate'),

]