from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    wish_status = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'


    def get_wish_status(self, obj, **kwargs):
        user_pk = self.context.get("user_pk")
        if obj.wish_event.filter(pk=user_pk).exists():
            return True
        return False
