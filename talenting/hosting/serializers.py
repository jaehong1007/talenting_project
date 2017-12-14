from rest_framework import serializers

from .models.hosting import Hosting, HostingPhoto, HostingReview, HostingRequest


class HostingPhotoSerializer(serializers.ModelSerializer):
    pk = serializers.PrimaryKeyRelatedField(read_only=True)
    place = serializers.PrimaryKeyRelatedField(read_only=True)
    hosting_thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = HostingPhoto
        fields = (
            'pk',
            'place',
            'hosting_image',
            'hosting_thumbnail',
            'caption',
            'type',
            'created_at',
        )


class HostingReviewSerializer(serializers.ModelSerializer):
    pk = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    host = serializers.PrimaryKeyRelatedField(read_only=True)
    place = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = HostingReview
        fields = (
            'pk',
            'author',
            'host',
            'place',
            'hosting_review',
            'recommend',
            'created_at',
        )


class HostingSerializer(serializers.ModelSerializer):
    pk = serializers.PrimaryKeyRelatedField(read_only=True)
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Hosting
        fields = (
            'pk',
            'owner',
            'category',
            'title',
            'summary',
            'primary_photo',
            'recommend_counter',
            'house_type',
            'room_type',
            'meal_type',
            'internet',
            'smoking',
            'pet',
            'rules',
            'language',
            'capacity',
            'min_stay',
            'max_stay',
            'description',
            'to_do',
            'exchange',
            'neighborhood',
            'transportation',
            'country',
            'city',
            'distinct',
            'street',
            'address',
            'postcode',
            'lat',
            'lon',
            'has_photo',
            'published',
            'created_at',
            'updated_at',
        )


class HostingRequestSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    place = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = HostingRequest
        fields = (
            'pk',
            'user',
            'place',
            'arrival_date',
            'departure_date',
            'number_travelers',
            'description',
            'created_at',
        )
