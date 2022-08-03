from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import mixins, generics

class CategoryMixinView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    generics.GenericAPIView
    ):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

category_view = CategoryMixinView.as_view()