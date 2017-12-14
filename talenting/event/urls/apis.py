from django.conf.urls import url


from ..apis import EventList, EventDetail, EventParticipateToggle, WishListEventToggle, EventPhotoList, EventPhotoDetail

urlpatterns = [
    url(r'^$', EventList.as_view(), name='event-list'),
    url(r'^(?P<event_pk>\d+)/$', EventDetail.as_view(), name='event-detail'),
    url(r'^(?P<event_pk>\d+)/participate/$', EventParticipateToggle.as_view(), name='event-participate'),
    url(r'^(?P<event_pk>\d+)/photo/$', EventPhotoList.as_view(), name='event-detail'),
    url(r'^(?P<event_pk>\d+)/photo/(?P<photo_pk>\d+)/$', EventPhotoDetail.as_view(), name='event-detail'),

    url(r'^(?P<event_pk>\d+)/wish-list-toggle/$', WishListEventToggle.as_view(), name='wish-list-add'),
]