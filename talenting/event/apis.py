from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.permissions import IsAuthorOrReadOnly
from .utils.pagination import EventPagination
from member.serializer import UserSerializer
from .serializer import EventSerializer, PhotoSerializer
from .models import Event, Photo


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
            'event': EventSerializer(instance).data,
            'result': participate_status,
        }
        return Response(data, status=status.HTTP_200_OK)


class EventPhotoList(APIView):
    queryset = Event.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, *args, **kwargs):
        event = get_object_or_404(Event, pk=kwargs['event_pk'])
        photos = event.photo_set.all()
        serializer = PhotoSerializer(photos, many=True)
        data = {
            'event': serializer.data,
            'code': 200,
            'msg': '',
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = PhotoSerializer(data=request.data)
        event = get_object_or_404(Event, pk=kwargs['event_pk'])
        if serializer.is_valid(raise_exception=True):
            serializer.save(place=event)
            data = {
                'event': serializer.data,
                'code': 201,
                'msg': '',
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventPhotoDetail(APIView):
    queryset = Event.objects.all()
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