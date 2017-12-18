from django.conf.urls import url

from ..apis import HostingList, HostingDetail, PhotoList, PhotoDetail, HostingReviewList, HostingReviewDetail, \
    WishListHostingToggle, HostingRequestDetail, HostingRequestList, HostingRequestAccept, HostingOptionsView

urlpatterns = [
    url(r'^$', HostingList.as_view(), name='hosting-list'),
    url(r'^(?P<hosting_pk>\d+)/$', HostingDetail.as_view(), name='hosting-detail'),
    url(r'^(?P<hosting_pk>\d+)/photo/$', PhotoList.as_view(), name='photo-list'),
    url(r'^(?P<hosting_pk>\d+)/photo/(?P<photo_pk>\d+)/$', PhotoDetail.as_view(), name='photo-detail'),
    url(r'^(?P<hosting_pk>\d+)/review/$', HostingReviewList.as_view(), name='review-list'),
    url(r'^(?P<hosting_pk>\d+)/review/(?P<review_pk>\d+)/$', HostingReviewDetail.as_view(), name='review-detail'),
    url(r'^(?P<hosting_pk>\d+)/wish-list-toggle/$', WishListHostingToggle.as_view(), name='wish-list-add'),
    url(r'^(?P<hosting_pk>\d+)/request/$', HostingRequestList.as_view(), name='request-list'),
    url(r'^(?P<hosting_pk>\d+)/request/(?P<request_pk>\d+)/$', HostingRequestDetail.as_view(), name='request-detail'),
    url(r'^(?P<hosting_pk>\d+)/request/(?P<request_pk>\d+)/accept/$', HostingRequestAccept.as_view(),
        name='request-accept'),
    url(r'^options/$', HostingOptionsView.as_view(), name='hosting-options'),
]
