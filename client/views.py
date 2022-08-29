from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins
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
    generics.GenericAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
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
            logger.warning(search)
            try:
                client_instance = Client.objects.get(Q(main_phone__icontains=search) | Q(alternative_phone__icontains=search))
            except Client.DoesNotExist:
                return Response({'Not found :('}, status=200)
            except:
                return Response({'Error :('}, status=404)
            serialized_client = ClientBasicSerializer(client_instance, many=False)
            logger.warning(serialized_client.data)
            return Response(serialized_client.data)
        elif 'email' in request.query_params:
            search = request.query_params.get('email')
            try:
                client_instance = Client.objects.get(Q(email__icontains=search) | Q(alternative_email__icontains=search))
            except Client.DoesNotExist:
                return Response({'Not found :('}, status=200)
            except:
                return Response({'Error :('}, status=404)
            serialized_client = ClientBasicSerializer(client_instance, many=False)
            return Response(serialized_client.data)
        else:
            return Response({'Unkown search'}, status=404)
    return Response({'not found'}, status=404)


@api_view(['GET', 'POST'])
def call_create_list_view(request, *args, **kwargs):
    logger.warning(request.data)
    method = request.method
    if method == "GET":
        if 'query_self' in request.query_params:
            limit = request.query_params.get('query_self')
            queryset = Call.objects.filter(id_user=request.user.id)[:int(limit)]
            data = CallSerializer(queryset, many=True).data
            return Response(data)
        queryset = Call.objects.all()
        data = CallSerializer(queryset, many=True).data
        return Response(data)
    if method == "POST":
        data = request.data
        try:
            if data['agent_email'] != '':
                user_instance = User.objects.get(email=data['agent_email'])
        except User.DoesNotExist:
            return Response({'Unknown user'}, status=200)
        data.pop('agent_email')
        data['id_user'] = user_instance.id
        # create an item
        serializer = CallSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
        return Response({"invalid": "not good data"}, status=400)


