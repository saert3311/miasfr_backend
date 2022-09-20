import datetime

from rest_framework import filters
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins
from rest_framework.pagination import PageNumberPagination
from .serializers import *
from common.models import User
from django.db.models import Count
import logging

from .models import Client

logger = logging.getLogger(__name__)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class ClientListAPIView(generics.ListAPIView):
    queryset = Client.objects.all().exclude(anon=True)
    serializer_class = ClientListSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'email', 'alternative_email', 'main_phone', 'alternative_phone']
    ordering_fields = ['first_name', 'last_name']
    ordering = ['first_name', 'last_name']

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

class AllCallsView(
    mixins.ListModelMixin,
    generics.GenericAPIView
    ):
    queryset = Call.objects.all()[:200]
    serializer_class = CallSerializer
    pagination_class = StandardResultsSetPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


all_calls_view = AllCallsView.as_view()

class ResumeCallsView(APIView):
    def get(self, request, format=None):
        range = request.query_params.get('range')
        inbound = Count('call', filter=Q(call__answered=True, call__direction='I'))
        outbound = Count('call', filter=Q(call__answered=True, call__direction='O'))
        missed = Count('call', filter=Q(call__answered=False, call__direction='I'))
        not_answered = Count('call', filter=Q(call__answered=False, call__direction='O'))
        today = datetime.datetime.today()
        if range == 'today':
           ranged_queryset = User.objects.filter(call__date_time__day=today.day)
        elif range == 'week':
           ranged_queryset = User.objects.filter(call__date_time__gte=today - datetime.timedelta(days=7))
        elif range == 'month':
            ranged_queryset = User.objects.filter(call__date_time__month=today.month)
        elif range == 'year':
            ranged_queryset = User.objects.filter(call__date_time__year=today.year)
        else:
            ranged_queryset = User.objects.all()
        queryset = ranged_queryset.annotate(inbound=inbound).annotate(outbound=outbound).annotate(missed=missed)\
            .annotate(not_answered=not_answered)
        if queryset.exists():
            serialized_queryset = CallResumeSerializer(queryset, many=True)
            return Response(serialized_queryset.data)
        return Response({'error': 'No Data'}, status=200)

resume_calls_view = ResumeCallsView.as_view()




