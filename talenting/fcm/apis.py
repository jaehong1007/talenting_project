from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from fcm.serializer import FcmMessageSerializer

User = get_user_model()


class SendMessage(APIView):
    authentication_classes = (TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        to_user = get_object_or_404(User, pk=request.data.get('to_user'))
        devices = to_user.fcmdevice_set.all()

        serializer = FcmMessageSerializer(
            data=request.data,
            context={
                'from_user': request.user,
                'to_user' : to_user,
            })
        if serializer.is_valid(raise_exception=True):
            devices.send_message(title=serializer.validated_data['title'],
                                 body=serializer.validated_data['body'])
            serializer.save()
            print(serializer.data)
            data = {
                'sent_message': serializer.data,
                'code': 201,
                'msg': 'message sent'
            }
            return Response(data, status=status.HTTP_201_CREATED)

# class MessageList(APIView):
#
