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


class HostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostingReview
        fields = (
            'author',
            'host',
            'place',
            'review',
            'recommend',
            'created_at',
        )


class HostingSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField('_get_photos')
    reviews = serializers.SerializerMethodField('_get_reviews')

    def _get_photos(self, obj):
        serializer = PhotoSerializer(obj.get_photos(), many=True)
        return serializer.data

    def _get_reviews(self, obj):
        serializer = PhotoSerializer(obj.get_hosting_reviews(), many=True)
        return serializer.data

    class Meta:
        model = Hosting
        fields = (
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
