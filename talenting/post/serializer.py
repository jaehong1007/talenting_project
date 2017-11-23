from rest_framework import serializers

from member.models import Event


class EventSerializer(serializers.ModelSerializer):
    # author = UserSerializer()

    class Meta:
        model = Event
        fields = (
            'pk',
            'photo',
            # 'author',
            'created_at',
            'updated_at',
        )
