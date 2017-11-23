from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .tasks import send_mail_task
from .serializer import SignUpSerializer


class SignUp(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            cur_site = get_current_site(request)
            email = serializer.validated_data['email']
            subject = 'welcome to Talenting!'
            message = render_to_string('registration/user_activate_email.html', {
                'user': user,
                'domain': cur_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': PasswordResetTokenGenerator().make_token(user),
            })
            send_mail_task.delay(
                subject=subject,
                message=message,
                recipient=email
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
