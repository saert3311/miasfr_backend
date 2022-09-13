from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins
from rest_framework.pagination import PageNumberPagination
from .serializers import *
from common.models import User
import logging

from .models import Client

logger = logging.getLogger(__name__)

class ClientListAPIView(generics.ListAPIView):
    queryset = Client.objects.all().exclude(anon=True)
    serializer_class = ClientListSerializer

client_list_view = ClientListAPIView.as_view()

class ClientRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

client_retrieve_view = ClientRetrieveAPIView.as_view()

class ClientCreateAPIView(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

client_create_view = ClientCreateAPIView.as_view()

class AnonClientCreateAPIView(
    mixins.CreateModelMixin,
    generics.GenericAPIView
    ):
    queryset = Client.objects.all()
    serializer_class = ClientAnonSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

anon_client_create_view = AnonClientCreateAPIView.as_view()

class AddressCreateAPIView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSaveSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

address_create_view = AddressCreateAPIView.as_view()


@api_view(['GET'])
def single_client_view(request, *args, **kwargs):
    method = request.method
    if method == 'GET':
        if 'phone' in request.query_params:
            search = request.query_params.get('phone')
            client_instance = Client.objects.filter(Q(main_phone__icontains=search) | Q(alternative_phone__icontains=search))
            if not client_instance.exists():
                return Response({'Not found :('}, status=200)
            serialized_client = ClientBasicSerializer(client_instance.first(), many=False)
            return Response(serialized_client.data)
        elif 'email' in request.query_params:
            search = request.query_params.get('email')
            client_instance = Client.objects.filter(Q(email__icontains=search) | Q(alternative_email__icontains=search))
            if not client_instance.exists():
                return Response({'Not found :('}, status=200)
            serialized_client = ClientBasicSerializer(client_instance.first(), many=False)
            return Response(serialized_client.data)
        else:
            return Response({'Unkown search'}, status=404)
    return Response({'not found'}, status=404)


@api_view(['GET', 'POST'])
def call_create_list_view(request, *args, **kwargs):
    method = request.method
    if method == "GET":
        paginator = PageNumberPagination()
        paginator.page_size = 10
        queryset = Call.objects.filter(id_user=request.user.id)
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = CallSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    if method == "POST":
        data = request.data
        if data['agent_email'] != '':
            try:
                user_instance = User.objects.get(email=data['agent_email'])
            except User.DoesNotExist:
                return Response({'Unknown user'}, status=200)
            data.pop('agent_email')
            data['id_user'] = user_instance.id
            # create an item
            serializer = CallSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'result':'created'}, status=200)
        return Response({"invalid": "not good data"}, status=400)

class LastCallDetailView(APIView):
    def get(self, request, format=None):
        call = Call.objects.filter(id_user=request.user.id)
        if call.exists():
            serialized_call = CallClientSerializer(call.first(), many=False)
            return Response(serialized_call.data)
        return Response({'error':'No Data'}, status=400)


last_call_info_view = LastCallDetailView.as_view()




