import random
import string

from django.contrib.auth import authenticate
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# from django.utils.encoding import force_bytes
# from django.utils.http import urlsafe_base64_encode
from django.contrib.auth import get_user_model
from rest_framework import status, generics
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.exceptions import APIException
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from event.models import Event
from hosting.models.hosting import Hosting
from member.models import Profile, ProfileImage, GuestReview
from utils.api import MyRetrieveUpdateDestroyAPIView, MyCreateAPIView, MyRetrieveUpdateAPIView, MyListCreateAPIView, \
    MyListAPIView
from utils.exception.api_exception import LogInException
from utils.permissions import IsAuthorOrReadOnly, IsProfileUserOrReadOnly, IsPlaceOwnerOrReadOnly, IsProfileOwner
from .serializer import SignUpSerializer, LogInSerializer, ProfileManageSerializer, ProfileImageSerializer, \
    ProfileSerializer, GuestReviewSerializer, WishHostingSerializer, WishEventSerializer, PasswordResetSerializer, \
    EventParticipateSerializer

from .tasks import send_mail_task

User = get_user_model()


class SignUp(APIView):

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            # Test의 편의성을 위해 임시로 가입하는 사람은 전부 active 처리
            user.is_active = True
            user.save()
            Profile.objects.create(user=user)

            '''
            임시로 블락처리
            # 인증메일 보낼 양식
            cur_site = get_current_site(request)
            email = serializer.validated_data['email']
            subject = 'welcome to Talenting!'
            # template파일을 이용, 변수들을 담아서 메세지 변수로 저장
            message = render_to_string('registration/user_activate_email.html', {
                'user': user,
                'domain': cur_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': PasswordResetTokenGenerator().make_token(user),
            })
            # celery를 이용한 비동기처리
            send_mail_task.delay(
                subject=subject,
                message=message,
                recipient=email
            )
            '''
            data = {
                'user': serializer.data,
                'code': status.HTTP_201_CREATED,
                'msg': ''
            }
            return Response(data=data, status=status.HTTP_201_CREATED)


class LogIn(APIView):

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']

        user = authenticate(
            email=email,
            password=password,
        )
        if user:
            data = {
                'token': user.token,
                'user': LogInSerializer(user).data,
                'code': status.HTTP_200_OK,
                'msg': ''
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            raise LogInException('사용자 인증 실패')


class EmailIsUnique(APIView):
    def post(self, request, *args, **kwargs):
        input_email = request.data['email']
        import re
        pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        data = dict(
            code=status.HTTP_200_OK,
            msg='사용가능한 이메일입니다.'
        )
        if not re.match(pattern, input_email):
            data['code'] = status.HTTP_400_BAD_REQUEST
            data['msg'] = '올바르지 않은 이메일 형식입니다.'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        elif User.objects.filter(email=input_email).exists():
            data['code'] = status.HTTP_400_BAD_REQUEST
            data['msg'] = '이미 가입되어 있는 이메일입니다.'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_200_OK)


class PasswordMissing(APIView):
    def rand_name(self):
        printable = string.printable[:62]
        return "".join([random.choice(printable) for _ in range(10)])

    def put(self, request, *args, **kwargs):
        email = request.data['email']
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        user = get_object_or_404(User, email=email, first_name=first_name, last_name=last_name)
        new_password = self.rand_name()
        user.set_password(new_password)
        user.save()
        subject = 'Talenting password reset information'
        message = f'Your password for talenting has been changed to {new_password}. You may log in with ' \
                  f'this temporary password and change the password for later use'
        # 실제 서비스할때는 비동기 처리 해주자
        send_mail_task(
            subject=subject,
            message=message,
            recipient=email
        )
        data = {
            'user': LogInSerializer(user).data,
            'code': status.HTTP_200_OK,
            'msg': '',
        }
        return Response(data=data, status=status.HTTP_200_OK)


class PasswordReset(generics.UpdateAPIView):
    authentication_classes = (BasicAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordResetSerializer

    def get_object(self):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            if not user.check_password(serializer.data.get("old_password")):
                raise APIException('Try again with the right password')
            user.set_password(serializer.data['new_password2'])
            user.save()
            data = {
                'user': LogInSerializer(user).data,
                'code': status.HTTP_200_OK,
                'msg': ''
            }
            return Response(data=data, status=status.HTTP_200_OK)


class ProfileRetrieveUpdate(MyRetrieveUpdateAPIView):
    authentication_classes = (BasicAuthentication, TokenAuthentication,)
    queryset = Profile.objects.all()
    serializer_class = ProfileManageSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProfileSerializer(instance)
        data = {
            self.model_name(): serializer.data,
            'code': status.HTTP_200_OK,
            'msg': ''
        }
        return Response(data=data, status=status.HTTP_200_OK)


class ProfileImageCreate(MyCreateAPIView):
    authentication_classes = (BasicAuthentication, TokenAuthentication,)
    queryset = ProfileImage.objects.all()
    serializer_class = ProfileImageSerializer

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


class ProfileImageRetrieveUpdateDelete(MyRetrieveUpdateDestroyAPIView):
    authentication_classes = (BasicAuthentication, TokenAuthentication,)
    queryset = ProfileImage.objects.all()
    serializer_class = ProfileImageSerializer
    permission_classes = (IsProfileUserOrReadOnly,)


class GuestReviewCreate(MyListCreateAPIView):
    authentication_classes = (BasicAuthentication, TokenAuthentication,)
    queryset = GuestReview.objects.all()
    serializer_class = GuestReviewSerializer

    def perform_create(self, serializer):
        guest = User.objects.get(pk=self.kwargs['pk'])
        review = serializer.save(host=self.request.user, guest=guest)
        if review.recommend:
            guest.recommendatons += 1
            guest.save()


class EventParticipateList(APIView):
    authentication_classes = (BasicAuthentication, TokenAuthentication,)
    permission_classes = (IsProfileOwner,)

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        self.check_object_permissions(self.request, user)

        participate_event = user.participants.all()
        serializer = EventParticipateSerializer(participate_event, many=True)
        data = {
            'event': serializer.data,
            'code': status.HTTP_200_OK,
            'msg': 'success'
        }
        return Response(data=data, status=status.HTTP_200_OK)


class WishListRetrieve(APIView):
    authentication_classes = (BasicAuthentication, TokenAuthentication,)
    permission_classes = (IsProfileOwner,)

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        self.check_object_permissions(self.request, user)

        wish_hostings = user.wish_hosting.all()
        wish_events = user.wish_event.all()
        wish_profiles = user.wish_profile.all()

        wish_hostings_serializer = WishHostingSerializer(wish_hostings, many=True)
        wish_event_serializer = WishEventSerializer(wish_events, many=True)
        wish_profile_serializer = ProfileSerializer(wish_profiles, many=True)

        data = {
            'hosting': wish_hostings_serializer.data,
            'event': wish_event_serializer.data,
            'profile': wish_profile_serializer.data,
            'code': status.HTTP_200_OK,
            'msg': ''
        }
        return Response(data, status=status.HTTP_200_OK)


class HostingWishListDelete(APIView):
    authentication_classes = (BasicAuthentication, TokenAuthentication,)
    permission_classes = (IsProfileOwner,)

    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        self.check_object_permissions(self.request, user)

        selected_hosting = get_object_or_404(Hosting, pk=kwargs['hosting_pk'])
        user.wish_hosting.remove(selected_hosting)
        return Response(status=status.HTTP_200_OK)


class EventWishListDelete(APIView):
    authentication_classes = (BasicAuthentication, TokenAuthentication,)
    permission_classes = (IsProfileOwner,)

    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        self.check_object_permissions(self.request, user)

        selected_event = get_object_or_404(Event, pk=kwargs['event_pk'])
        user.wish_event.remove(selected_event)
        return Response(status=status.HTTP_200_OK)


class ProfileWishListDelete(APIView):
    authentication_classes = (BasicAuthentication, TokenAuthentication,)
    permission_classes = (IsProfileOwner,)

    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        self.check_object_permissions(self.request, user)

        selected_profile = get_object_or_404(Event, pk=kwargs['profile_pk'])
        user.wish_event.remove(selected_profile)
        return Response(status=status.HTTP_200_OK)


class WishListAddHosting(generics.GenericAPIView):
    queryset = Profile.objects.all()

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        data = {
            'user': user.pk,
            'hosting': instance.pk
        }
        if not user.wish_hosting.filter(pk=instance.pk).exists():
            user.wish_hosting.add(instance)
            data.extend({
                'code': status.HTTP_201_CREATED,
                'msg': 'Added on the wish list'
            })
        else:
            user.wish_hosting.remove(instance)
            data.extend({
                'code': status.HTTP_201_CREATED,
                'msg': "Get deleted from the wish list"
            })
        return Response(data=data, status=status.HTTP_200_OK)
