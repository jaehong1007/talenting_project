from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from fcm.models import Chat
from fcm.serializer import MessageSerializer, ChatListSerializer

User = get_user_model()


class SendMessage(APIView):
    authentication_classes = (TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        to_user = get_object_or_404(User, pk=request.data['to_user'])
        filtered_chat = Chat.objects.filter(Q(start_user=request.user) | Q(target_user=request.user))
        chat = filtered_chat.filter(Q(start_user=to_user) | Q(target_user=to_user))

        if not chat:
            chat = Chat.start(request.user, to_user)
        else:
            chat = chat[0]
            if chat.start_user == request.user:
                to_user = chat.target_user
            else:
                to_user = chat.start_user
        devices = to_user.fcmdevice_set.all()
        serializer = MessageSerializer(data=request.data,
                                       context={'chat': chat, 'from_user': request.user})
        if serializer.is_valid(raise_exception=True):
            devices.send_message(title='Talenting',
                                 body=serializer.validated_data['body'])
            serializer.save()
            data = {
                'sent_message': serializer.data,
                'code': 201,
                'msg': 'message sent'
            }
            return Response(data, status=status.HTTP_201_CREATED)


class ChatRecord(APIView):
    authentication_classes = (TokenAuthentication,)

    def get(self, request, *args, **kwargs):
        chat = get_object_or_404(Chat, pk=kwargs['chat_pk'])
        messages = chat.messages.all()
        serializer = MessageSerializer(messages, many=True)
        data = {
            'messages': serializer.data,
            'code': 200,
            'msg': ''
        }
        return Response(data=data, status=status.HTTP_200_OK)


class ChatList(APIView):
    authentication_classes = (TokenAuthentication,)

    def get(self, request, *args, **kwargs):
        chats = Chat.objects.filter(Q(start_user=request.user) | Q(target_user=request.user))
        messages = [chat.messages.first() for chat in chats]
        serializer = ChatListSerializer(messages, many=True, context={'user': request.user})
        data = {
            'chat': serializer.data,
            'code': 200,
            'msg': ''
        }
        return Response(data=data, status=status.HTTP_200_OK)
