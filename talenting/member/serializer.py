from rest_framework import serializers

from .models import User, Profile, ProfileImage


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


class LogInSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'email', 'password')
        read_only_fields = ('password',)


class ProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'birth', 'gender', 'self_intro', 'talent_category',
                  'talent_intro', 'country', 'city', 'occupation', 'available_languages')
        read_only_fields = ('user',)


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = ('pk', 'image', 'created_at')


class ProfileSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField('_get_images')
    age = serializers.SerializerMethodField('_calculate_age')

    def _get_images(self, obj):
        serializers = ProfileImageSerializer(obj.get_images(), many=True)
        return serializers.data

    def _calculate_age(self, obj):
        if obj.birth:
            return obj.calculate_age()
        return None

    class Meta:
        model = Profile
        fields = ('user', 'birth', 'gender', 'self_intro', 'talent_category',
                  'talent_intro', 'country', 'city', 'occupation',
                  'available_languages', 'images', 'age')
        read_only_fields = ('user',)
