from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import *
from rest_framework import mixins, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

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
        print(request.data)
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

item_create_view = ItemCreateMixinView.as_view()

class ItemListMixinView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Item.objects.exclude(active=False)
    serializer_class = ItemListSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['category__name']

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

item_list_view = ItemListMixinView.as_view()

class PeriodMixinView(
    mixins.ListModelMixin,
    generics.GenericAPIView):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

period_list_view = PeriodMixinView.as_view()

@api_view(['POST'])
def creation_test(request, *args, **kwargs):
    print(request.data)
    return Response({'result': 'recieved'}, status=200)