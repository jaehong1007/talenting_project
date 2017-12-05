from rest_framework import status, generics, mixins
from rest_framework.response import Response


class BaseCreateAPIView(mixins.CreateModelMixin):
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = {
            self.model_name(): serializer.data,
            'code': status.HTTP_200_OK,
            'msg': ''
        }
        return Response(data=data, status=status.HTTP_201_CREATED, headers=headers)


class BaseRetrieveAPIView(mixins.RetrieveModelMixin):
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = {
            self.model_name(): serializer.data,
            'code': status.HTTP_200_OK,
            'msg': ''
        }
        return Response(data=data, status=status.HTTP_200_OK)


class BaseUpdateAPIView(mixins.UpdateModelMixin):
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

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


class MyBaseAPIView(generics.GenericAPIView):
    def model_name(self):
        serializer_class = self.get_serializer_class()
        model = str(serializer_class.Meta.model).split('.')[-1][:-2].lower()
        return model

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super().get_serializer(*args, **kwargs)


class MyRetrieveUpdateAPIView(BaseRetrieveAPIView,
                              BaseUpdateAPIView,
                              MyBaseAPIView):
    pass


class MyRetrieveUpdateDestroyAPIView(MyRetrieveUpdateAPIView,
                                     mixins.DestroyModelMixin,
                                     MyBaseAPIView):
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class MyCreateAPIView(BaseCreateAPIView, MyBaseAPIView):
    pass
