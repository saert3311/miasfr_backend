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

class ItemCreateMixinView(
    mixins.CreateModelMixin,
    generics.GenericAPIView
    ):
    queryset = Item.objects.all()
    serializer_class = ItemCreationSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

item_create_view = ItemCreateMixinView.as_view()

class ItemListMixinView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Item.objects.exclude(active=False)
    serializer_class = ItemListSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

item_list_view = ItemListMixinView.as_view()