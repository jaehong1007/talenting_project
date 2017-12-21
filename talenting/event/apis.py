from django.db.models import Q
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication, BaseAuthentication, BasicAuthentication

from rest_framework.response import Response
from rest_framework.views import APIView

from utils.api import MyRetrieveUpdateDestroyAPIView
from utils.permissions import IsAuthorOrReadOnly, IsEventOwnerOrReadOnly
from .utils.pagination import EventPagination
from member.serializer import UserSerializer, MyEventSerializer
from .serializer import EventParticipateSerializer, EventPhotoSerializer

from .models import Event, EventPhoto, EventComment
from .serializer import EventSerializer
from .utils.permissions import IsOwnerOrReadOnly

User = get_user_model()


class EventList(APIView):
    """
    List hosting posts or create a hosting post.

    * Authenticate with token or username/password.
    * Allow owner to perform any method.
    * Only safe method is available for who is not owner.
    """
    authentication_classes = (TokenAuthentication, BaseAuthentication)
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        queryset = Event.objects.all()
        search_query = self.request.query_params.get('search_query', None)
        if search_query is not None:
            queryset = queryset.filter(
                Q(address__icontains=search_query)
            )
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = EventSerializer(queryset, many=True, context={'user_pk': request.user.pk})
        data = {
            'event': serializer.data,
            'code': 200,
            'msg': '',
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            data = {
                'event': serializer.data,
                'code': 201,
                'msg': '',
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class EventDetail(APIView):
    """
    Retrieve, update and delete a hosting post.

    * Authenticate with token or username/password.
    * Allow owner to perform any method.
    * Only safe method is available for who is not owner.
    """
    authentication_classes = (TokenAuthentication, BaseAuthentication)
    permission_classes = (IsOwnerOrReadOnly,)

    def get_object(self, pk):
        obj = get_object_or_404(Event, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        event = self.get_object(pk=kwargs['event_pk'])
        serializer = EventSerializer(event, context={'user_pk': request.user.pk})
        data = {
            'event': serializer.data,
            'code': 200,
            'msg': '',
        }
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        event = self.get_object(pk=kwargs['event_pk'])
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = {
                'event': serializer.data,
                'code': 200,
                'msg': '',
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        event = self.get_object(pk=kwargs['event_pk'])
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class EventList(generics.ListCreateAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#     pagination_class = EventPagination
#     authentication_classes = (TokenAuthentication,)
#
#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)
#
#     def get_serializer_context(self):
#         return {
#             'request': self.request,
#             'format': self.format_kwarg,
#             'view': self,
#             'user_pk': self.request.user.pk
#         }
#
#
# class EventDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Event.objects.all()
#     lookup_url_kwarg = 'event_pk'
#     serializer_class = EventSerializer
#     permission_classes = (
#         IsAuthorOrReadOnly,
#     )
#     authentication_classes = (TokenAuthentication,)
#
#     def get_serializer_context(self):
#         return {
#             'request': self.request,
#             'format': self.format_kwarg,
#             'view': self,
#             'user_pk': self.request.user.pk
#         }


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


class EventPhotoList(APIView):
    authentication_classes = (TokenAuthentication, BaseAuthentication)
    permission_classes = (IsAuthorOrReadOnly,)

    def get(self, request, *args, **kwargs):
        event = get_object_or_404(Event, pk=kwargs['event_pk'])
        photos = event.eventphoto_set.all()
        serializer = EventPhotoSerializer(photos, many=True)
        data = {
            'event_photo': serializer.data,
            'code': 200,
            'msg': '',
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = EventPhotoSerializer(data=request.data)
        event = get_object_or_404(Event, pk=kwargs['event_pk'])
        if serializer.is_valid(raise_exception=True):
            serializer.save(events=event)
            data = {
                'event_photo': serializer.data,
                'code': 201,
                'msg': '',
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventPhotoDetail(MyRetrieveUpdateDestroyAPIView):
    authentication_classes = (BasicAuthentication, TokenAuthentication,)
    queryset = EventPhoto.objects.all()
    serializer_class = EventPhotoSerializer
    permission_classes = (IsAuthorOrReadOnly,)


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


class EventCreatedList(APIView):
    authentication_classes = (BasicAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthorOrReadOnly,)

    def get(self, request, *args, **kwargs):
        event = Event.objects.filter(author=request.user)
        serializer = MyEventSerializer(event, many=True)
        data = {
            'event': serializer.data,
            'code': status.HTTP_200_OK,
            'msg': 'success'
        }
        return Response(data=data, status=status.HTTP_200_OK)


class CommentCreateList(generics.ListCreateAPIView):
    queryset = EventComment.objects.all()
    serializer_class = EventSerializer
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentDetail(APIView):
    """
    Retrieve, update and delete a hosting post.

    * Authenticate with token or username/password.
    * Allow owner to perform any method.
    * Only safe method is available for who is not owner.
    """
    authentication_classes = (TokenAuthentication, BaseAuthentication)
    permission_classes = (IsOwnerOrReadOnly,)

    def get_object(self, pk):
        obj = get_object_or_404(EventComment, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        comment = self.get_object(pk=kwargs['comment_pk'])
        serializer = EventSerializer(comment, context={'user_pk': request.user.pk})
        data = {
            'event': serializer.data,
            'code': 200,
            'msg': '',
        }
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        comment = self.get_object(pk=kwargs['comment_pk'])
        serializer = EventSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = {
                'event': serializer.data,
                'code': 200,
                'msg': '',
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        comment = self.get_object(pk=kwargs['comment_pk'])
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
