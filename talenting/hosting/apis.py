from django.contrib.auth import get_user_model

from django.db.models import Q
from rest_framework import status, generics
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from hosting import options
from utils.permissions import IsOwnerOrReadOnly, IsPlaceOwnerOrReadOnly, IsAuthorOrReadOnly

from .serializers import HostingSerializer, HostingPhotoSerializer, HostingReviewSerializer, HostingRequestSerializer
from .models.hosting import Hosting, HostingPhoto, HostingReview, HostingRequest

User = get_user_model()


class HostingList(APIView):
    """
    List hosting posts or create a hosting post.

    * Authenticate with token or username/password.
    * Allow owner to perform any method.
    * Only safe method is available for who is not owner.
    """
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        queryset = Hosting.objects.all()
        search_query = self.request.query_params.get('search_query', None)
        if search_query is not None:
            queryset = queryset.filter(
                Q(address__icontains=search_query)
            )
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = HostingSerializer(queryset, many=True, context={'user_pk': request.user.pk})
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


#
# class HostingListOwn(generics.ListAPIView):
#     authentication_classes = (TokenAuthentication, BasicAuthentication)
#     permission_classes = (IsOwnerOrReadOnly,)
#     serializer_class = HostingSerializer
#
#     queryset = Hosting.objects.all()
#
#     def get_object(self):





class HostingDetail(APIView):
    """
    Retrieve, update and delete a hosting post.

    * Authenticate with token or username/password.
    * Allow owner to perform any method.
    * Only safe method is available for who is not owner.
    """
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsOwnerOrReadOnly,)

    def get_object(self, pk):
        obj = get_object_or_404(Hosting, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        hosting = self.get_object(pk=kwargs['hosting_pk'])
        # 세준 임시 추가
        serializer = HostingSerializer(hosting, context={'user_pk': request.user.pk})
        # This is hard coding for API structure for Android.
        data = {
            'hosting': serializer.data,
            'code': 200,
            'msg': '',
        }
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        hosting = self.get_object(pk=kwargs['hosting_pk'])
        serializer = HostingSerializer(hosting, data=request.data, partial=True)
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

    * Authenticate with token or username/password.
    * Allow owner to perform any method.
    * Only safe method is available for who is not owner.
    """
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsPlaceOwnerOrReadOnly,)

    def get(self, request, *args, **kwargs):
        hosting = get_object_or_404(Hosting, pk=kwargs['hosting_pk'])
        photos = hosting.hostingphoto_set.all()
        serializer = HostingPhotoSerializer(photos, many=True)
        # This is hard coding for API structure for Android.
        data = {
            'hosting_photo': serializer.data,
            'code': 200,
            'msg': '',
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = HostingPhotoSerializer(data=request.data)
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

    * Authenticate with token or username/password.
    * Allow owner to perform any method.
    * Only safe method is available for who is not owner.
    """
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsPlaceOwnerOrReadOnly,)

    def get_object(self, pk):
        obj = get_object_or_404(HostingPhoto, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        photo = self.get_object(pk=kwargs['photo_pk'])
        serializer = HostingPhotoSerializer(photo)
        # This is hard coding for API structure for Android.
        data = {
            'hosting_photo': serializer.data,
            'code': 200,
            'msg': '',
        }
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        photo = self.get_object(pk=kwargs['photo_pk'])
        serializer = HostingPhotoSerializer(photo, data=request.data, partial=True)
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

    * Authenticate with token or username/password.
    * Allow owner to perform any method.
    * Only safe method is available for who is not owner.
    """
    authentication_classes = (TokenAuthentication, BasicAuthentication)
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
        if HostingRequest.objects.filter(user=request.user, place=hosting).exists():
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
        raise PermissionDenied('Sorry, you are not allowed to write a review on this place')


class HostingReviewDetail(APIView):
    """
    Retrieve, update, delete a hosting review.

    * Authenticate with token or username/password.
    * Allow owner to perform any method.
    * Only safe method is available for who is not owner.
    """
    authentication_classes = (TokenAuthentication, BasicAuthentication)
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
        if review.is_editable:
            serializer = HostingReviewSerializer(review, data=request.data, partial=True)
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
        raise PermissionDenied('Sorry, your review update period is over')

    def delete(self, request, *args, **kwargs):
        review = self.get_object(pk=kwargs['review_pk'])
        if review.is_editable:
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise PermissionDenied('Sorry, your review update period is over')


class HostingOptionsView(APIView):
    """
    Return hosting options, for example, HOUSE_TYPES and ROOM_TYPES.
    Take option name from request parameter and get hosting options by using it.
    """

    def get(self, request, *args, **kwargs):
        options_name = self.request.query_params.get('param', None)
        if options_name is not None:
            option = getattr(options, options_name.upper(), False)
            types = []
            if option:
                for item in option:
                    types.append({'code': item[0], 'value': item[1]})
                data = {
                    options_name: types,
                    'code': 200,
                    'msg': '',
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                raise NotFound("No match")
        else:
            raise NotFound("Please check your parameter variable.")


class HostingRequestList(APIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        hosting = get_object_or_404(Hosting, pk=kwargs['hosting_pk'])
        hosting_request = get_object_or_404(HostingRequest, user=request.user, place=hosting)
        serializer = HostingRequestSerializer(hosting_request)
        # This is hard coding for API structure for Android.
        data = {
            'hosting_request': serializer.data,
            'code': 200,
            'msg': '',
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        hosting = get_object_or_404(Hosting, pk=kwargs['hosting_pk'])
        if not HostingRequest.objects.filter(user=request.user, place=hosting).exists():
            serializer = HostingRequestSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user, place=hosting)
                data = {
                    'hosting_request': serializer.data,
                    'code': 201,
                    'msg': '',
                }
                return Response(data, status=status.HTTP_201_CREATED)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        raise PermissionDenied("You've already sent request to stay to this host")


class HostingRequestDetail(APIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticated)

    def get_object(self, pk):
        obj = get_object_or_404(HostingRequest, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def delete(self, request, *args, **kwargs):
        hosting_request = self.get_object(pk=kwargs['request_pk'])
        hosting_request.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HostingRequestAccept(APIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsPlaceOwnerOrReadOnly,)

    def put(self, request, *args, **kwargs):
        hosting_request = get_object_or_404(HostingRequest, pk=kwargs['request_pk'])
        self.check_object_permissions(self.request, hosting_request)
        hosting_request.accepted = True
        hosting_request.save(update_fields=['accepted'])
        serializer = HostingRequestSerializer(hosting_request)
        data = {
            'hosting_request': serializer.data,
            'code': 200,
            'msg': '',
        }
        return Response(data, status=status.HTTP_200_OK)


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

class WishListHostingToggle(generics.GenericAPIView):
    queryset = Hosting.objects.all()
    lookup_url_kwarg = 'hosting_pk'

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        data = {
            'user': user.pk,
            'hosting': instance.pk,
        }
        if not user.wish_hosting.filter(pk=instance.pk).exists():
            user.wish_hosting.add(instance)
            data.update({
                'code': status.HTTP_200_OK,
                'msg': 'Added on the wish list'
            })
        else:
            user.wish_hosting.remove(instance)
            data.update({
                'code': status.HTTP_200_OK,
                'msg': "Get deleted from the wish list"
            })
        return Response(data=data, status=status.HTTP_200_OK)
