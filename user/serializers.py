from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=5, max_length=20, write_only=True, style={'input_type':'password'})
    confirm_password = serializers.CharField(min_length=5)
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'confirm_password']

    def validate(self, data):
        username = data.get('username')
        first_name = data.get('first_name')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if first_name and first_name.isupper():
            raise  serializers.ValidationError({'first_name':"First Name should not contain uppercase letter"})

        if password != confirm_password:
            raise  serializers.ValidationError({'password':"Password does not match", 'confirm_password':"Password does not match"})

        if not username.isalnum():
            raise serializers.ValidationError({'username':"Username must only contain alphanumeric letters"})

        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=5, style={'input_type':'password'}, write_only=True)
    username = serializers.CharField(read_only=True)  # Add username as a read-only field
    access_token = serializers.CharField(read_only=True)  # Add access_token as a read-only field

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user_data = User.objects.filter(email=email).first()
        if user_data:
            user = authenticate(
                request=self.context.get("request"),
                email=email,
                password=password,
            )
            if not user:
                raise serializers.ValidationError({'AuthorizationError':'Invalid Credentials provided\nPlease check the provided credentials'})

            user_token = user.token()

            return {
            'username': user.username,
            'email': user.email,
            'access_token': str(user_token.get('access')),
            'refresh_token':str(user_token.get('refresh'))
        }

        else:
            raise serializers.ValidationError({'AuthorizationError':'Invalid User'})
