from rest_framework import serializers

from .models import Event, Photo


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = (
            '__all__'
        )


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Photo
        fields = ('event', 'image')
