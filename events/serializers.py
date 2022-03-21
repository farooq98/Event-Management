from rest_framework import serializers
from .models import Event
from user_registration.serializers import UserSerializer


class EventSerializer(serializers.ModelSerializer):

    owner = UserSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'location', 'owner']