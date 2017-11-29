from rest_framework import serializers

from .models import Hosting, Photo


class HostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hosting
        fields = (
            '__all__'
        )


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            '__all__'
        )
