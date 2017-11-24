from django.shortcuts import get_object_or_404
from rest_framework import generics, authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from event.permissions import IsAuthorOrReadOnly
from .serializer import EventSerializer
from .models import Event


class EventList(generics.ListCreateAPIView):

    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (
        IsAuthorOrReadOnly,
    )












