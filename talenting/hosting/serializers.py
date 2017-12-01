from rest_framework import serializers

from .models import Hosting, Photo, HostingReview


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            'pk',
            'image',
            'caption',
            'type',
        )


class HostingReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostingReview
        fields = (
            'pk',
            'author',
            'host',
            'place',
            'review',
            'recommend',
            'created_at',
        )


class HostingSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True)
    reviews = HostingReviewSerializer(many=True)

    class Meta:
        model = Hosting
        fields = (
            'pk',
            'owner',
            'category',
            'title',
            'summary',
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
            'active',
            'published',
            'created_at',
            'updated_at',
            'photos',
            'reviews',
        )
