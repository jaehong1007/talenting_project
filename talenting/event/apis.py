from rest_framework import generics, status
from rest_framework.response import Response

from member.serializer import UserSerializer
from .models import Event, Photo
from .serializer import EventSerializer
from .utils.pagination import EventPagination
from .utils.permissions import IsOwnerOrReadOnly


class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    pagination_class = EventPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'user_pk': self.request.user.pk
        }


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    lookup_url_kwarg = 'event_pk'
    serializer_class = EventSerializer
    permission_classes = (
        IsOwnerOrReadOnly,
    )

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'user_pk': self.request.user.pk
        }


class EventParticipateToggle(generics.GenericAPIView):
    queryset = Event.objects.all()
    lookup_url_kwarg = 'event_pk'

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if user in instance.participants.filter(pk=user.pk):
            instance.participants.remove(user)
            participate_status = False
        else:
            instance.participants.add(user)
            participate_status = True
        data = {
            'participant': UserSerializer(user).data,
            'event': EventSerializer(instance).data,
            'result': participate_status,
        }
        return Response(data)


class EventPhoto(generics.ListCreateAPIView):
    queryset = Photo.objects.all()


class WishListEventToggle(generics.GenericAPIView):
    queryset = Event.objects.all()
    lookup_url_kwarg = 'event_pk'

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        data = {
            'user': user.pk,
            'event': instance.pk,
        }
        if not user.wish_event.filter(pk=instance.pk).exists():
            user.wish_event.add(instance)
            data.update({
                'code': status.HTTP_200_OK,
                'msg': 'Added on the wish list'
            })
        else:
            user.wish_event.remove(instance)
            data.update({
                'code': status.HTTP_200_OK,
                'msg': "Get deleted from the wish list"
            })
        return Response(data=data, status=status.HTTP_200_OK)
