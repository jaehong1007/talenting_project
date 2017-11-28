from rest_framework import serializers

from .models import Hosting


class HostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hosting
        fields = (
            '__all__'
        )


