from rest_framework import serializers

from .models.hosting import Hosting, HostingPhoto, HostingReview, HostingRequest


class HostingPhotoSerializer(serializers.ModelSerializer):
    place = serializers.PrimaryKeyRelatedField(read_only=True)  # hosting_pk
    hosting_thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = HostingPhoto
        fields = ('pk', 'place', 'hosting_image', 'hosting_thumbnail',
                  'caption', 'type', 'created_at',)


class HostingReviewSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)  # user_pk
    host = serializers.PrimaryKeyRelatedField(read_only=True)  # user_pk
    place = serializers.PrimaryKeyRelatedField(read_only=True)  # hosting_pk

    class Meta:
        model = HostingReview
        fields = ('pk', 'author', 'host', 'place',
                  'hosting_review', 'recommend', 'created_at',)

    def create(self, validated_data):
        obj = HostingReview.objects.create(**validated_data)
        return obj


class HostingSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)  # user_pk
    wish_status = serializers.SerializerMethodField()  # True or False

    class Meta:
        model = Hosting

        fields = ('owner', 'category', 'title', 'summary', 'primary_photo',
                  'recommend_counter', 'house_type', 'room_type', 'meal_type', 'internet',
                  'smoking', 'pet', 'rules', 'language', 'capacity', 'min_stay', 'max_stay',
                  'description', 'to_do', 'exchange', 'neighborhood', 'transportation',
                  'country', 'city', 'distinct', 'street', 'address', 'postcode', 'lat',
                  'lon', 'has_photo', 'published', 'created_at', 'updated_at', 'wish_status',)

    def get_wish_status(self, obj, **kwargs):
        """
        Check existence of wish-hosting in member with user_pk.
        """
        user_pk = self.context.get("user_pk")  # get user.pk from HostingSerializer.context
        if obj.wish_hosting.filter(pk=user_pk).exists():  # Hosting.wish_hosting.filter
            return True
        return False


class HostingRequestSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # user_pk
    place = serializers.PrimaryKeyRelatedField(read_only=True)  # hosting_pk

    class Meta:
        model = HostingRequest
        fields = ('pk', 'user', 'host', 'place', 'arrival_date', 'departure_date',
                  'number_travelers', 'description', 'accepted', 'created_at',)
