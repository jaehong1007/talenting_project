from django.conf.urls import url

from ..apis import EventList, EventDetail, EventParticipateToggle, WishListEventToggle, EventPhotoList, \
    EventPhotoDetail, CommentCreateList, EventCreatedList, CommentDetail

urlpatterns = [
    url(r'^$', EventList.as_view(), name='event-list'),
    url(r'^(?P<event_pk>\d+)/$', EventDetail.as_view(), name='event-detail'),
    url(r'^(?P<event_pk>\d+)/participate/$', EventParticipateToggle.as_view(), name='event-participate'),
    url(r'^(?P<event_pk>\d+)/photo/$', EventPhotoList.as_view(), name='event-detail'),
    url(r'^(?P<event_pk>\d+)/photo/(?P<photo_pk>\d+)/$', EventPhotoDetail.as_view(), name='event-detail'),

    url(r'^(?P<event_pk>\d+)/wish-list-toggle/$', WishListEventToggle.as_view(), name='wish-list-add'),
    url(r'^(?P<event_pk>\d+)/comment/$', CommentCreateList.as_view(), name='comment_list'),
    url(r'^(?P<event_pk>\d+)/comment/(?P<comment_pk>\d+)/$', CommentDetail.as_view(), name='comment_detail'),
    url(r'^created/$', EventCreatedList.as_view(), name='event-created'),
]