from rest_framework import generics, status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from .utils.pagination import EventPagination
from .utils.permissions import IsOwnerOrReadOnly
from member.serializer import UserSerializer
from .serializer import EventSerializer
from .models import Event, Photo


class EventList(generics.ListCreateAPIView):

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    pagination_class = EventPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    lookup_url_kwarg = 'event_pk'
    serializer_class = EventSerializer
    permission_classes = (
        IsOwnerOrReadOnly,
    )


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



class WishListAddEvent(generics.GenericAPIView):
    queryset = Event.objects.all()
    lookup_url_kwarg = 'event_pk'

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if not user.wish_event.filter(pk=instance.pk).exists():
            user.wish_event.add(instance)
        else:
            raise APIException('This event is already in my wish list items')
        data = {
            'user': user.pk,
            'event': instance.pk,
            'code': status.HTTP_201_CREATED,
            'msg': ''
        }
        return Response(data=data, status=status.HTTP_201_CREATED)






