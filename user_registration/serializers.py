from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['mobile_number', 'email', 'username', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
