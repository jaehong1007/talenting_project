from rest_framework import serializers

from member.serializer import UserSerializer
from .models import Event, Photo


class EventSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    wish_status = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_wish_status(self, obj, **kwargs):
        user_pk = self.context.get("user_pk")
        if obj.wish_event.filter(pk=user_pk).exists():
            return True
        return False


class PhotoSerializer(serializers.ModelSerializer):
    pk = serializers.ReadOnlyField()
    event = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = Photo
        fields = (
            '__all__'
        )
