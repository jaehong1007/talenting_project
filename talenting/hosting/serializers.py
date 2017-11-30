from rest_framework import serializers

from .models import Hosting, Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            'pk',
            'image',
            'caption',
            'type',
        )


class HostingSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField('_get_photos')

    def _get_photos(self, obj):
        serializer = PhotoSerializer(obj.get_photos(), many=True)
        return serializer.data

    # reviews = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Hosting
        fields = (
            'owner',
            'category',
            'title',
            'photos',
        )
