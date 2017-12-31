from django.shortcuts import render

# Create your views here.


from django.contrib.auth.models import User
from django.db import models

from uuidfield import UUIDField

from . import permissions

class Chat(models.Model):
    uuid = UUIDField(auto=True)
    started = models.DateTimeField('started', editable=False, auto_now_add=True)
    users = models.ManyToManyField(User, related_name='chats', through='UserChatStatus')

    def __unicode__(self):
        users_str = ', '.join([user.username for user in self.users.all()])
        message_count = len(self.messages.all())
        return "{users} - {message_count} messages (started {started})".format(users=users_str,
                                                                               message_count=message_count,
                                                                               started=self.started)

    @classmethod
    def start(cls, chat_user, users):
        chat_users = [chat_user,] + users
        chat = cls()
        chat.save()
        chat.add_users(chat_users)
        return chat

    def add_users(self, users):
        for user in users:
            user_chat_status = UserChatStatus(user=user, chat=self)
            user_chat_status.save()

    def add_message(self, user_from, message):
        message = Message(chat=self, user_from=user_from, message_body=message)
        message.save()
        return message


class UserChatStatus(models.Model):
    INACTIVE = 'inactive'
    ACTIVE = 'active'
    ARCHIVED = 'archived'
    CHAT_STATUS_CHOICES = (
        (INACTIVE, 'Inactive'),
        (ACTIVE, 'Active'),
        (ARCHIVED, 'Archived'),
    )

    user = models.ForeignKey(User, related_name='user_chat_statuses')
    chat = models.ForeignKey(Chat, related_name='user_chat_statuses')
    status = models.CharField(max_length=8, choices=CHAT_STATUS_CHOICES, default=ACTIVE)
    joined = models.DateTimeField('joined_timestamp', editable=False, auto_now_add=True)


class Message(models.Model):
    uuid = UUIDField(auto=True)
    timestamp = models.DateTimeField('timestamp', editable=False, auto_now_add=True)
    chat = models.ForeignKey(Chat, related_name='messages')
    user_from = models.ForeignKey(User, related_name='messages')
    message_body = models.TextField()

    def __unicode__(self):
        return "{user} says \"{message}\" ({timestamp})".format(user=self.user_from, message=self.message_body, timestamp=self.timestamp)

    def save(self):
        super(Message, self).save() # First save this model, so that we have an id
        for user in self.chat.users.all().exclude(id=self.user_from.id):
            if self.chat.user_chat_statuses.get(user=user).status == UserChatStatus.ACTIVE:
                 UserMessageStatus.objects.create(user=user, message=self, is_read=True)
            else:
                 UserMessageStatus.objects.create(user=user, message=self)