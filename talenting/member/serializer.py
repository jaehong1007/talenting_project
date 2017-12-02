from rest_framework import serializers

from .models import User, Profile


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'email', 'password',
                  )
        read_only_fields = ('password',)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'self_intro', 'my_talent', 'city', 'occupation',
                  'available_languages', 'profile_image')
        read_only_fields = ('user',)
