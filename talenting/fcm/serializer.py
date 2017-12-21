from django.contrib.auth import get_user_model
from django.db.models import Q
from fcm_django.api.rest_framework import UniqueRegistrationSerializerMixin, DeviceViewSetMixin, AuthorizedMixin
from fcm_django.models import FCMDevice
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet

from fcm.models import Message, Chat
from member.models import Profile
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


# class FcmMessageSerializer(serializers.ModelSerializer):
#     from_user = serializers.SerializerMethodField()
#     sent_by = serializers.CharField(read_only=True)
#     body = serializers.CharField()
#     created_at = serializers.DateTimeField(read_only=True)
#
#     def get_from_user(self, obj):
#         return self.context.get("from_user").pk
#
#     def get_to_user(self, obj):
#         return obj.pk
#
#     def create(self, validated_data):
#         return Message.objects.create(
#             from_user=self.context.get("from_user"),
#             to_user=self.context.get("to_user"),
#             **validated_data)
#
#     def to_representation(self, instance):
#         ret = super().to_representation(instance)
#         ret['to_user'] = self.context.get("to_user").pk
#         return ret
#
#     class Meta:
#         model = Message
#         fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        profile = Profile.objects.get(pk=ret['from_user']['pk'])
        image = profile.images.first()
        if image:
            ret['from_user']['image'] = image.profile_thumbnail.url
        else:
            ret['from_user']['image'] = None
        return ret

    def create(self, validated_data):
        chat = self.context['chat']
        from_user = self.context['from_user']
        message = chat.add_message(from_user=from_user, body=validated_data['body'])
        return message

    class Meta:
        model = Message
        fields = ('from_user', 'body', 'sent_by', 'created_at',)
        read_only_fields = ('sent_by', 'created_at')


class ChatListSerializer(serializers.ModelSerializer):
    target_user = serializers.SerializerMethodField()
    pk = serializers.SerializerMethodField()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        profile = Profile.objects.get(pk=ret['target_user']['pk'])
        image = profile.images.first()
        if image:
            ret['target_user']['image'] = image.profile_thumbnail.url
        else:
            ret['target_user']['image'] = None
        return ret

    def get_target_user(self, obj):
        if self.context['user'] == obj.chat.start_user:
            target_user = obj.chat.target_user
        else:
            target_user = obj.chat.start_user
        return UserSerializer(target_user).data

    def get_pk(self, obj):
        return obj.chat.pk

    class Meta:
        model = Message
        fields = ('pk', 'target_user', 'body', 'created_at',)
