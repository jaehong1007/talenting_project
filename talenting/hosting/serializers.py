from rest_framework import serializers

from .models.hosting import Hosting, HostingPhoto, HostingReview
from .countries import COUNTRIES


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
    # 세준 임시 추가
    wish_status = serializers.SerializerMethodField()

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
            'min_lat',
            'max_lat',
            'min_lon',
            'max_lon',
            'has_photo',
            'published',
            'created_at',
            'updated_at',
            # 세준 임시 추가
            'wish_status',
        )

    # 세준 임시 추가
    def get_wish_status(self, obj, **kwargs):
        user_pk = self.context.get("user_pk")
        if obj.wish_hosting.filter(pk=user_pk).exists():
            return True
        return False
