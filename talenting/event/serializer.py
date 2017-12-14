from rest_framework import serializers

from member.serializer import UserSerializer
from .models import Event, Photo


class EventSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    event_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    closing_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    opening_date = serializers.DateTimeField(format='%Y-%m-%d')
    wish_status = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_wish_status(self, obj, **kwargs):
        user_pk = self.context.get("user_pk")
        if obj.wish_event.filter(pk=user_pk).exists():
            return True
        return False


class EventParticipateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = (
            'id',
            'author',
            'title',
            'participants'
        )


class PhotoSerializer(serializers.ModelSerializer):
    pk = serializers.PrimaryKeyRelatedField(read_only=True)
    events = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Photo
        fields = (
            'pk',
            'events',
            'image'
        )
