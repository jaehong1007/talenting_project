from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.permissions import IsOwnerOrReadOnly

from .serializers import HostingSerializer
from .models import Hosting


class HostingList(generics.ListCreateAPIView):
    """
    List hosting post or create a new hosting post
    """
    queryset = Hosting.objects.all()
    serializer_class = HostingSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class HostingDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, delete a hosting post
    """
    queryset = Hosting.objects.all()
    serializer_class = HostingSerializer
    permission_classes = (IsOwnerOrReadOnly,)

# class HostingList(APIView):
#     """
#     List hosting post or create a new hosting post
#     """
#
#     def get(self, request, *args, **kwargs):
#         hostings = Hosting.objects.all()
#         serializer = HostingSerializer(hostings, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request, *args, **kwargs):
#         serializer = HostingSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


# class HostingDetail(APIView):
#     """
#     Retrieve, update, delete a hosting post
#     """
#
#     def get(self, request, *args, **kwargs):
#         hosting = Hosting.objects.get(pk=self.kwargs['pk'])
#         serializer = HostingSerializer(hosting)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request, *args, **kwargs):
#         hosting = Hosting.objects.get(pk=self.kwargs['pk'])
#         serializer = HostingSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, *args, **kwargs):
#         hosting = Hosting.objects.get(pk=self.kwargs['pk'])
#         self.delete(hosting)
#         return Response(status=status.HTTP_204_NO_CONTENT)
