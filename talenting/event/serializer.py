from rest_framework import serializers

from member.serializer import UserSerializer
from .models import Event, Photo


class EventSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Event
        fields = (
            '__all__'
        )


class PhotoSerializer(serializers.ModelSerializer):
    pk = serializers.ReadOnlyField()
    event = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = Photo
        fields = (
            'pk',
            'event',
            'image')
