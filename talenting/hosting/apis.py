from rest_framework import status, generics, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsOwnerOrReadOnly, IsPlaceOwnerOrReadOnly

from .serializers import HostingSerializer, PhotoSerializer, HostingReviewSerializer
from .models import Hosting, Photo, HostingReview


class HostingPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class HostingList(APIView):
    """
    List hosting posts or create a hosting post.
    """
    permission_classes = (IsOwnerOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, *args, **kwargs):
        hostings = Hosting.objects.all()
        serializer = HostingSerializer(hostings, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = HostingSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def get_model_name(self):
        return 'hosting'


class HostingDetail(APIView):
    """
    Retrieve, update and delete a hosting post.

    * Allow owner to perform any method.
    * Only safe method is available for who is not owner.
    """
    permission_classes = (IsOwnerOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self, pk):
        obj = get_object_or_404(Hosting, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        hosting = self.get_object(kwargs['hosting_pk'])
        serializer = HostingSerializer(hosting)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        hosting = self.get_object(kwargs['hosting_pk'])
        serializer = HostingSerializer(hosting, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        hosting = self.get_object(kwargs['hosting_pk'])
        hosting.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_model_name(self):
        return 'hosting'


class PhotoList(APIView):
    """
    List photos linked with hosting object or create a photo.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsPlaceOwnerOrReadOnly,)

    def get(self, request, *args, **kwargs):
        hosting = get_object_or_404(Hosting, pk=kwargs['hosting_pk'])
        photos = hosting.photo_set.all()
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_model_name(self):
        return 'photo'


class PhotoDetail(APIView):
    """
    Retrieve, update and delete a photo.

    * Allow owner to perform any method.
    * Only safe method is available for who is not owner.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsPlaceOwnerOrReadOnly,)

    def get_object(self, pk):
        obj = get_object_or_404(Photo, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        photo = self.get_object(kwargs['photo_pk'])
        serializer = PhotoSerializer(photo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        photo = self.get_object(kwargs['photo_pk'])
        serializer = PhotoSerializer(photo, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        photo = self.get_object(kwargs['photo_pk'])
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_model_name(self):
        return 'photo'


class HostingReviewList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsPlaceOwnerOrReadOnly,)

    def get(self, request, *args, **kwargs):
        hosting = get_object_or_404(Hosting, pk=kwargs['hosting_pk'])
        reviews = hosting.hostingreview_set.all()
        serializer = HostingReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = HostingReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def get_model_name(self):
        return 'review'


class HostingReviewDetail(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsPlaceOwnerOrReadOnly,)

    def get_object(self, pk):
        obj = get_object_or_404(HostingReview, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        review = self.get_object(pk=kwargs['review_pk'])
        serializer = HostingReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        review = self.get_object(pk=kwargs['review_pk'])
        serialzier = HostingReviewSerializer(review, data=request.data)
        if serialzier.is_valid(raise_exception=True):
            serialzier.save()
            return Response(serialzier.data, status=status.HTTP_200_OK)
        return Response(serialzier.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        review = self.get_object(pk=kwargs['review_pk'])
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_model_name(self):
        return 'review'

# class HostingList(generics.ListCreateAPIView):

# """
#     List hosting post or create a new hosting post
#     """
#     queryset = Hosting.objects.all()
#     serializer_class = HostingSerializer
#     # authentication_classes = (TokenAuthentication)`
#     permission_classes = (IsOwnerOrReadOnly,)
#     pagination_class = HostingPagination
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)


# class HostingDetail(generics.RetrieveUpdateDestroyAPIView):
#     """
#     Retrieve, update, delete a hosting post
#     """
#     queryset = Hosting.objects.all()
#     lookup_url_kwarg = 'hosting_pk'
#     serializer_class = HostingSerializer
#     # authentication_classes = (TokenAuthentication)
#     permission_classes = (IsOwnerOrReadOnly,)


# class PhotoList(generics.ListCreateAPIView):
#     queryset = Photo.objects.all()
#     serializer_class = PhotoSerializer
#     permission_classes = (IsPhotoOwnerOrReadOnly,)
#
#     def perform_create(self, serializer):
#         serializer.save(place=self.request.data['hosting'])
#
#
# class PhotoDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Photo.objects.all()
#     lookup_url_kwarg = 'photo_pk'
#     serializer_class = PhotoSerializer
#     permission_classes = (IsPhotoOwnerOrReadOnly,)
