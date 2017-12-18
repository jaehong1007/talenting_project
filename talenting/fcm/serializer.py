from django.contrib.auth import get_user_model
from fcm_django.api.rest_framework import UniqueRegistrationSerializerMixin, DeviceViewSetMixin, AuthorizedMixin
from fcm_django.models import FCMDevice
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet

from fcm.models import FcmMessage
from member.serializer import UserSerializer

User = get_user_model()


class FCMDeviceSerializer(serializers.ModelSerializer, UniqueRegistrationSerializerMixin):
    active = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    class Meta:
        model = FCMDevice
        fields = (
            "id", "registration_id", "active",
            "date_created", "type"
        )
        read_only_fields = ("date_created",)

    def get_active(self, obj):
        return True

    def get_type(self, obj):
        return 'android'


class FCMDeviceViewSet(DeviceViewSetMixin, ModelViewSet):
    queryset = FCMDevice.objects.all()
    serializer_class = FCMDeviceSerializer


class FCMDeviceAuthorizedViewSet(AuthorizedMixin, FCMDeviceViewSet):
    pass


class FcmMessageSerializer(serializers.Serializer):
    from_user = serializers.SerializerMethodField()
    sent_by = serializers.CharField(read_only=True)
    title = serializers.CharField()
    body = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)

    def get_from_user(self, obj):
        return self.context.get("from_user").pk

    def get_to_user(self, obj):
        return obj.pk

    def create(self, validated_data):
        return FcmMessage.objects.create(
            from_user=self.context.get("from_user"),
            to_user=self.context.get("to_user"),
            **validated_data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['to_user'] = self.context.get("to_user").pk
        return ret

# class FcmMessageList