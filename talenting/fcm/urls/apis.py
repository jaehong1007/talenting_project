from django.conf.urls import url

from fcm.apis import SendMessage
from ..serializer import FCMDeviceAuthorizedViewSet
urlpatterns = [
    url(r'^device/$', FCMDeviceAuthorizedViewSet.as_view({'post': 'create'}), name='create_fcm_device'),
    url(r'^send-message/$', SendMessage.as_view(), name='send-message'),
]
