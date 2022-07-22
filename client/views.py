from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .serializers import *

from .models import Client

class AllClientsList(APIView):
    def get(self, request, format=None):
        queryset = Client.objects.all()
        serializer = ClientSerializerList(queryset, many=True)
        return Response(serializer.data)

class ClientDetailAPIView(generics.RetrieveAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializerFull

client_detail_view = ClientDetailAPIView.as_view()


# Usar perform_create para añadir info de usuario antes de guardar generics.CreateAPIView
