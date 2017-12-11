from rest_framework import serializers, response, status

from .models.hosting import Hosting, Photo, HostingReview


# class HostingListSerializer(serializers.ListSerializer):
#     @property
#     def data(self):
#         serialized_data = super(HostingListSerializer, self).data
#         custom_representation = {
#             'hosting': serialized_data,
#             'code': response.status_code,
#             'msg': '',
#         }
#         return custom_representation


class PhotoSerializer(serializers.ModelSerializer):
    pk = serializers.ReadOnlyField()
    place = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Photo
        fields = (
            'pk',
            'place',
            'hosting_image',
            'caption',
            'type',
        )


class HostingReviewSerializer(serializers.ModelSerializer):
    pk = serializers.ReadOnlyField()
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
    pk = serializers.ReadOnlyField()
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
            'min_lat',
            'max_lat',
            'min_lon',
            'max_lon',
            'has_photo',
            'published',
            'created_at',
            'updated_at',
        )
        # list_serializer_class = HostingListSerializer
