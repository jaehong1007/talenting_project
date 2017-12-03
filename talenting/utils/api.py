from rest_framework import status, generics, mixins
from rest_framework.response import Response


class MyBaseAPIView(generics.GenericAPIView):
    def model_name(self):
        serializer_class = self.get_serializer_class()
        model = str(serializer_class.Meta.model).split('.')[-1][:-2].lower()
        return model

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super().get_serializer(*args, **kwargs)


class MyRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView,
                                     MyBaseAPIView):

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = {
            self.model_name(): serializer.data,
            'code': status.HTTP_200_OK,
            'msg': ''
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        data = {
            self.model_name(): serializer.data,
            'code': status.HTTP_200_OK,
            'msg': ''
        }
        return Response(data=data, status=status.HTTP_200_OK)
