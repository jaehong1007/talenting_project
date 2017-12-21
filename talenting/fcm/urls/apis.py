from django.conf.urls import url

from fcm.apis import SendMessage, ChatRecord, ChatList
from ..serializer import FCMDeviceAuthorizedViewSet
urlpatterns = [
    url(r'^device/$', FCMDeviceAuthorizedViewSet.as_view({'post': 'create'}), name='create_fcm_device'),
    url(r'^chat/send-message/$', SendMessage.as_view(), name='send-message'),
    url(r'^chat/(?P<chat_pk>\d+)/$', ChatRecord.as_view(), name='chat'),
    url(r'^chat-list/$', ChatList.as_view(), name='chat-list')
]
