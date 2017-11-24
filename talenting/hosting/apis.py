from rest_framework import generics

from .serializers import HostingSerializer
from .models import Hosting


class HostingList(generics.ListCreateAPIView):
    queryset = Hosting.objects.all()
    serializer_class = HostingSerializer
