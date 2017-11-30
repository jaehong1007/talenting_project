from django.contrib.auth import authenticate
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# from django.utils.encoding import force_bytes
# from django.utils.http import urlsafe_base64_encode
from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from member.models import Profile, ProfileImage
from utils.permissions import IsAuthorOrReadOnly
from .serializer import SignUpSerializer, LogInSerializer, ProfileCreateSerializer, ProfileSerializer, \
    ProfileImageSerializer

# from .tasks import send_mail_task

User = get_user_model()


class SignUp(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Test의 편의성을 위해 임시로 가입하는 사람은 전부 active 처리
            user.is_active = True
            user.save()

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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogIn(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']

        user = authenticate(
            email=email,
            password=password,
        )
        if user:
            token, token_created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'user': LogInSerializer(user).data,
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'message': '아이디 혹은 이메일이 올바르지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)


class EmailIsUnique(APIView):
    def post(self, request, *args, **kwargs):
        input_email = request.data['email']
        import re
        pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        if not re.match(pattern, input_email):
            return Response({'message': '유효하지 않은 이메일 형식입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        elif User.objects.filter(email=input_email).exists():
            return Response({'message': '이미 가입되어 있는 이메일입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': '유효한 이메일입니다.'}, status=status.HTTP_200_OK)


class ProfileCreate(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileCreateSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProfileManage(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer



# class Profile2(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer
#
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         if instance.birth:
#             age = instance.calculate_age()
#         else:
#             age = '알 수 없음'
#         serializer.data['age'] = age
#         return Response(serializer.data)
#
#     def update(self, request, *args, **kwargs):
#         kwargs['partial'] = True
#         return super().update(request, *args, **kwargs)


class ProfileImage(generics.CreateAPIView):
    queryset = ProfileImage.objects.all()
    serializer_class = ProfileImageSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)
