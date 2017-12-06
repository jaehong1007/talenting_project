from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .utils.pagination import EventPagination
from .utils.permissions import IsOwnerOrReadOnly, IsPhotoOwnerOrReadOnly
from member.serializer import UserSerializer
from .serializer import EventSerializer, PhotoSerializer
from .models import Event, Photo


class EventList(APIView):
    """
    List hosting posts or create a hosting post.

    * Authenticate with token.
    * Allow owner to perform any method.
    * Only safe method is available for who is not owner.
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get(self, request, *args, **kwargs):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        data = {
            'event': serializer.data,
            'code': 200,
            'msg': 'OK',
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(owner=request.user)
            data = {
                'hosting': serializer.data,
                'code': 201,
                'msg': 'CREATED',
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
# class EventList(generics.ListCreateAPIView):
#
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#     pagination_class = EventPagination
#
#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)


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
        return Response(data, status=status.HTTP_200_OK)


class EventPhotoList(APIView):
    """
    List photos linked with hosting object or create a photo.
    """

    permission_classes = (IsPhotoOwnerOrReadOnly,)

    def get(self, request, *args, **kwargs):
        event = get_object_or_404(Event, pk='pk')
        photos = event.photo_set.all()
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)