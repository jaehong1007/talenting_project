from django.contrib.auth import get_user_model
from rest_framework import status, generics, permissions
from rest_framework.authentication import TokenAuthentication, BaseAuthentication
from rest_framework.exceptions import APIException
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from member.serializer import UserSerializer
from utils.permissions import IsOwnerOrReadOnly, IsPlaceOwnerOrReadOnly

from .serializers import HostingSerializer, PhotoSerializer, HostingReviewSerializer
from .models.hosting import Hosting, Photo, HostingReview
from .paginator import Paginator, HostingPagination

User = get_user_model()


class HostingList(APIView):
    """
    List hosting posts or create a hosting post.

    * Authenticate with token.
    * Allow owner to perform any method.
    * Only safe method is available for who is not owner.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOwnerOrReadOnly,)

    def get(self, request, *args, **kwargs):
        hostings = Hosting.objects.all()
        serializer = HostingSerializer(hostings, many=True)
        # This is hard coding for API structure for Android.
        data = {
            'hosting': serializer.data,
            'code': 200,
            'msg': '',
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = HostingSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(owner=request.user)
            # This is hard coding for API structure for Android.
            data = {
                'hosting': serializer.data,
                'code': 201,
                'msg': '',
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class HostingDetail(APIView):
    """
    Retrieve, update and delete a hosting post.

    * Authenticate with token.
    * Allow owner to perform any method.
    * Only safe method is available for who is not owner.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOwnerOrReadOnly,)

    def get_object(self, pk):
        obj = get_object_or_404(Hosting, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        hosting = self.get_object(pk=kwargs['hosting_pk'])
        serializer = HostingSerializer(hosting)
        # This is hard coding for API structure for Android.
        data = {
            'hosting': serializer.data,
            'code': 200,
            'msg': '',
        }
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        hosting = self.get_object(pk=kwargs['hosting_pk'])
        serializer = HostingSerializer(hosting, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # This is hard coding for API structure for Android.
            data = {
                'hosting': serializer.data,
                'code': 200,
                'msg': '',
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        hosting = self.get_object(pk=kwargs['hosting_pk'])
        hosting.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PhotoList(APIView):
    """
    List photos linked with hosting object or create a photo.

    * Authenticate with token.
    * Allow owner to perform any method.
    * Only safe method is available for who is not owner.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsPlaceOwnerOrReadOnly,)

    def get(self, request, *args, **kwargs):
        hosting = get_object_or_404(Hosting, pk=kwargs['hosting_pk'])
        photos = hosting.photo_set.all()
        serializer = PhotoSerializer(photos, many=True)
        # This is hard coding for API structure for Android.
        data = {
            'hosting_photo': serializer.data,
            'code': 200,
            'msg': '',
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = PhotoSerializer(data=request.data)
        hosting = get_object_or_404(Hosting, pk=kwargs['hosting_pk'])
        if serializer.is_valid(raise_exception=True):
            serializer.save(place=hosting)
            # This is hard coding for API structure for Android.
            data = {
                'hosting_photo': serializer.data,
                'code': 201,
                'msg': '',
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhotoDetail(APIView):
    """
    Retrieve, update and delete a photo.

    * Authenticate with token.
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
        photo = self.get_object(pk=kwargs['photo_pk'])
        serializer = PhotoSerializer(photo)
        # This is hard coding for API structure for Android.
        data = {
            'hosting_photo': serializer.data,
            'code': 200,
            'msg': '',
        }
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        photo = self.get_object(pk=kwargs['photo_pk'])
        serializer = PhotoSerializer(photo, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # This is hard coding for API structure for Android.
            data = {
                'hosting_photo': serializer.data,
                'code': 200,
                'msg': '',
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        photo = self.get_object(pk=kwargs['photo_pk'])
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HostingReviewList(APIView):
    """
    List hosting reviews linked with hosting post or create a hosting review.

    * Authenticate with token.
    * Allow owner to perform any method.
    * Only safe method is available for who is not owner.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsPlaceOwnerOrReadOnly,)

    def get(self, request, *args, **kwargs):
        hosting = get_object_or_404(Hosting, pk=kwargs['hosting_pk'])
        reviews = hosting.hostingreview_set.all()
        serializer = HostingReviewSerializer(reviews, many=True)
        # This is hard coding for API structure for Android.
        data = {
            'hosting_review': serializer.data,
            'code': 200,
            'msg': '',
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        hosting = get_object_or_404(Hosting, pk=kwargs['hosting_pk'])
        host = get_object_or_404(User, pk=hosting.owner_id)
        serializer = HostingReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(
                author=request.user,
                host=host,
                place=hosting,
            )
            # This is hard coding for API structure for Android.
            data = {
                'hosting_review': serializer.data,
                'code': 200,
                'msg': '',
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class HostingReviewDetail(APIView):
    """
    Retrieve, update, delete a hosting review.

    * Authenticate with token.
    * Allow owner to perform any method.
    * Only safe method is available for who is not owner.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsPlaceOwnerOrReadOnly,)

    def get_object(self, pk):
        obj = get_object_or_404(HostingReview, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        review = self.get_object(pk=kwargs['review_pk'])
        serializer = HostingReviewSerializer(review)
        # This is hard coding for API structure for Android.
        data = {
            'hosting_review': serializer.data,
            'code': 200,
            'msg': '',
        }
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        review = self.get_object(pk=kwargs['review_pk'])
        serializer = HostingReviewSerializer(review, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # This is hard coding for API structure for Android.
            data = {
                'hosting_review': serializer.data,
                'code': 200,
                'msg': '',
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        review = self.get_object(pk=kwargs['review_pk'])
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class HostingList(generics.ListCreateAPIView):
#     """
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

class WishListAddHosting(generics.GenericAPIView):
    queryset = Hosting.objects.all()
    lookup_url_kwarg = 'hosting_pk'

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if not user.wish_hosting.filter(pk=instance.pk).exists():
            user.wish_hosting.add(instance)
        else:
            raise APIException('This hosting is already in my wish list items')
        data = {
            'user': user.pk,
            'hosting': instance.pk,
            'code': status.HTTP_201_CREATED,
            'msg': ''
        }
        return Response(data=data, status=status.HTTP_201_CREATED)