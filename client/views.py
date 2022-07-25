from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins
from .serializers import *

from .models import Client

class ClientListAPIView(generics.ListAPIView):
    queryset = Client.objects.all()
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
        print('Llamo create')
        serializer.save(user=self.request.user)

client_create_view = ClientCreateAPIView.as_view()

class AddressCreateAPIView(mixins.CreateModelMixin, generics.GenericAPIView):
    queeryset = Address.objects.all()
    serializer_class = AddressSaveSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

address_create_view = AddressCreateAPIView.as_view()




# Usar perform_create para añadir info de usuario antes de guardar generics.CreateAPIView
