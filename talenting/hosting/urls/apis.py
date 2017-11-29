from django.conf.urls import url

from ..apis import HostingList, HostingDetail

urlpatterns = [
    url(r'^$', HostingList.as_view(), name='hosting-list'),
    url(r'^(?P<hosting_pk>\d+)$', HostingDetail.as_view(), name='hosting-detail')
]