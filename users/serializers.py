from django.contrib.auth.models import User
from rest_framework import serializers

from sessions.serializers import SessionSerializer


class UserSerializer(serializers.ModelSerializer):
    attended_sessions = SessionSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'attended_sessions', 'first_name', 'last_name', 'email', 'date_joined']


