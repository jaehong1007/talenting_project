from django.contrib.auth import authenticate
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# from django.utils.encoding import force_bytes
# from django.utils.http import urlsafe_base64_encode
from django.contrib.auth import get_user_model
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from member.models import Profile, ProfileImage
from utils.api import MyRetrieveUpdateDestroyAPIView, MyCreateAPIView
from utils.exception.api_exception import LogInException
from utils.permissions import IsAuthorOrReadOnly
from .serializer import SignUpSerializer, LogInSerializer, ProfileManageSerializer, ProfileImageSerializer, \
    ProfileSerializer

# from .tasks import send_mail_task

User = get_user_model()


class SignUp(APIView):

    def get_fields_info(self):
        return 'user', SignUpSerializer.Meta.fields

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
            }
            message = {
                'code': status.HTTP_201_CREATED,
                'msg': ''
            }
            data.update(message)
            return Response(data=data, status=status.HTTP_201_CREATED)


class LogIn(APIView):

    def get_fields_info(self):
        return 'user', LogInSerializer.Meta.fields

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']

        user = authenticate(
            email=email,
            password=password,
        )
        if user:
            data = {
                'token':user.token,
                'user':LogInSerializer(user).data,
                'code': status.HTTP_201_CREATED,
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
            email=input_email,
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


class ProfileRetrieveUpdateDelete(MyRetrieveUpdateDestroyAPIView):
    def get_fields_info(self):
        return 'profile', ProfileManageSerializer.Meta.fields

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


class ProfileImage(MyCreateAPIView):
    def get_fields_info(self):
        return 'profileimage', ProfileImageSerializer.Meta.fields

    queryset = ProfileImage.objects.all()
    serializer_class = ProfileImageSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)
