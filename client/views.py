from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ClientSerializer

from .models import Client

class AllClientsList(APIView):
    def get(self, request, format=None):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)
