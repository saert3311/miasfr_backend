from django.shortcuts import redirect
from rest_framework import generics
from .serializers import UserDetailSerializer
from .models import User

def root_redirect(request):
    response = redirect('https://miamiscaffoldrental.com')
    return response

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

user_detail_view = UserDetail.as_view()