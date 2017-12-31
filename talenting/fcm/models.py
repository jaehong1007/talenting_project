from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


# def get_sentinel_user():
#     return get_user_model().objects.get_or_create(username='deleted')[0]


class Chat(models.Model):
    start_user = models.ForeignKey('member.User', related_name='start_user')
    target_user = models.ForeignKey('member.User', related_name='target_user')
    updated_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def start(cls, start_user, target_user):
        chat = cls()
        chat.start_user = start_user
        chat.target_user = target_user
        chat.save()
        return chat

    def add_message(self, from_user, body):
        message = Message(chat=self, from_user=from_user, body=body)
        message.save()
        self.updated_at = timezone.now()
        self.save()
        return message

    class Meta:
        ordering = ['-updated_at']


class Message(models.Model):
    from_user = models.ForeignKey('member.User',
                                  related_name='from_user')
    # on_delete=models.SET(get_sentinel_user))
    body = models.TextField()
    chat = models.ForeignKey(Chat, related_name='messages')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'sent by {self.from_user}'

    @property
    def sent_by(self):
        if self.from_user.is_host:
            return 'host'
        return 'guest'

    class Meta:
        ordering = ['-created_at']
