from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import serializers, generics
from rest_framework.permissions import AllowAny

from users.serializers import UserSerializer


# Create your views here.
class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    lookup_field = 'username'


    



