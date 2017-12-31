from rest_framework import serializers

from event.models import Event
from hosting.models.hosting import Hosting
from .models import Profile, ProfileImage, GuestReview, MyTrip

from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'email', 'first_name', 'last_name')


class SignUpSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('pk', 'email', 'password1', 'password2', 'first_name', 'last_name')

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('password should match')
        return data

    def create(self, validated_data):
        return self.Meta.model.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password2'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )


class PasswordResetSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError('password should match')
        if data['old_password'] == data['new_password1']:
            raise serializers.ValidationError('Old password and new password should be different')
        return data


class LogInSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('pk', 'email', 'password')


class ProfileManageSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'birth', 'gender', 'self_intro', 'talent_category',
                  'talent_intro', 'country', 'city', 'occupation', 'available_languages', 'age')
        read_only_fields = ('age',)

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name


class ProfileImageSerializer(serializers.ModelSerializer):
    profile_thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = ProfileImage
        fields = ('pk', 'image', 'profile_thumbnail', 'created_at')


class ProfileSerializer(serializers.ModelSerializer):
    images = ProfileImageSerializer(many=True)
    age = serializers.SerializerMethodField('_calculate_age')
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    recommendations = serializers.SerializerMethodField()
    wish_status = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('pk', 'first_name', 'last_name', 'birth', 'gender', 'self_intro', 'talent_category',
                  'talent_intro', 'country', 'city', 'occupation', 'available_languages', 'images', 'age',
                  'wish_status', 'recommendations')

    def _calculate_age(self, obj):
        if obj.birth:
            return obj.calculate_age()
        return None

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_wish_status(self, obj, **kwargs):
        user_pk = self.context.get("user_pk")
        if obj.wish_profile.filter(pk=user_pk).exists():
            return True
        return False

    def get_recommendations(self, obj):
        return obj.user.recommendations


class GuestReviewSerializer(serializers.ModelSerializer):
    host = UserSerializer(read_only=True)
    guest = UserSerializer(read_only=True)

    class Meta:
        model = GuestReview
        fields = ('host', 'guest', 'review', 'recommend', 'created_at')


class WishHostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hosting
        fields = ('pk', 'owner', 'title', 'primary_photo')


class WishEventSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Event
        fields = ('pk', 'author', 'title', 'primary_photo')


class MyEventSerializer(WishEventSerializer):
    pass


class MyTripSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = MyTrip
        fields = ('pk', 'user', 'destination', 'arrival_date', 'departure_date',
                  'number_travelers', 'description')
