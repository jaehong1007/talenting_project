from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class FcmMessage(models.Model):
    from_user = models.ForeignKey('member.User', related_name='from_user')
    to_user = models.ForeignKey('member.User', related_name='to_user')
    title = models.TextField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def sent_by(self):
        if self.from_user.is_host:
            return 'host'
        return 'guest'

    class Meta:
        ordering = ['-created_at']
