from django.db import models


class EventManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class Event(models.Model):
    photo = models.ImageField(upload_to='post')
    title = models.CharField(max_length=20)
    context = models.TextField(max_length=300, blank=True)
    # author = models.ForeignKey()
    country = models.CharField
    starting_date = models.DateTimeField()
    closing_date = models.DateTimeField()
    maximum_participant = models.IntegerField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = EventManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Evenet (PK: {self.pk})'


class EventComment(models.Model):
    # author = models.ForeignKey(
    #     on_delete=models.SET_NULL,
    #     blank=True
    # )
    event = models.ForeignKey(Event, related_name='comments')
    content = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']