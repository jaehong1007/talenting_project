from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication

from rest_framework.response import Response
from rest_framework.views import APIView

from utils.permissions import IsAuthorOrReadOnly, IsEventOwnerOrReadOnly
from .utils.pagination import EventPagination
from member.serializer import UserSerializer
from .serializer import EventSerializer, PhotoSerializer, EventParticipateSerializer

from .models import Event, Photo
from .serializer import EventSerializer
from .utils.pagination import EventPagination
from .utils.permissions import IsOwnerOrReadOnly


class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    pagination_class = EventPagination
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    lookup_url_kwarg = 'event_pk'
    serializer_class = EventSerializer
    permission_classes = (
        IsAuthorOrReadOnly,
    )
    authentication_classes = (TokenAuthentication,)


class EventParticipateToggle(generics.GenericAPIView):
    queryset = Event.objects.all()
    lookup_url_kwarg = 'event_pk'
    authentication_classes = (TokenAuthentication,)

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
            'event': EventParticipateSerializer(instance).data,
            'result': participate_status,
        }
        return Response(data, status=status.HTTP_200_OK)


class EventPhotoList(generics.ListCreateAPIView):
    queryset = Event.objects.all
    serializer_class = PhotoSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class EventPhotoDetail(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthorOrReadOnly,)

    def get_object(self, pk):
        obj = get_object_or_404(Photo, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        photo = self.get_object(pk=kwargs['photo_pk'])
        serializer = PhotoSerializer(photo)
        data = {
            'hosting': serializer.data,
            'code': 200,
            'msg': '',
        }
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        photo = self.get_object(pk=kwargs['photo_pk'])
        serializer = PhotoSerializer(photo, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = {
                'hosting': serializer.data,
                'code': 200,
                'msg': '',
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        photo = self.get_object(pk=kwargs['photo_pk'])
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
