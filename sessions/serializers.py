from django.contrib.auth.models import User
from django.utils import timezone

from rest_framework import serializers

from sessions.models import Session


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'

    def validate_event_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError('Given date can not be past.')
        return value


