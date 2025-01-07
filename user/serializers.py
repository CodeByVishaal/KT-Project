from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=5, max_length=20, write_only=True)
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def validate(self, data):
        username = data.get('username', '')
        first_name = data.get('first_name', '')

        if first_name and first_name.isupper():
            raise  serializers.ValidationError({'first_name':"First Name should not contain uppercase letter"})


        if not username.isalnum():
            raise serializers.ValidationError({'username':"Username must only contain alphanumeric letters"})

        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
