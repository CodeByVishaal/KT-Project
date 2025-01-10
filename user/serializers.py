from rest_framework import serializers
# from rest_framework.exceptions import AuthenticationFailed
from .models import User
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=5, max_length=20, write_only=True, style={'input_type':'password'})
    confirm_password = serializers.CharField(min_length=5, write_only=True, )
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
        validated_data.pop('confirm_password', None)
        return User.objects.create_user(**validated_data)

class AdminRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=5, max_length=20, write_only=True, style={'input_type':'password'})
    confirm_password = serializers.CharField(min_length=5, write_only=True)
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
        validated_data.pop('confirm_password', None)
        return User.objects.create_superuser(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=5, style={'input_type':'password'}, write_only=True)
    username = serializers.CharField(read_only=True)
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)

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
            'refresh_token':str(user_token.get('refresh')),
            }

        else:
            raise serializers.ValidationError({'AuthorizationError':'Invalid User'})

class UpdateUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False, min_length=4)
    current_password = serializers.CharField(required=True, min_length=5, write_only=True)
    new_password = serializers.CharField(required=False, min_length=5, write_only=True)
    confirm_password = serializers.CharField(required=False, min_length=5, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'current_password', 'new_password', 'confirm_password']

    def validate(self, data):
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        user = self.context['request'].user

        if not user.check_password(current_password):
            raise serializers.ValidationError({'current_password':"Incorrect Password"})

        if new_password or confirm_password:
            if new_password != confirm_password:
                raise serializers.ValidationError({'password': "Passwords do not match"})

        return data


    def update(self, instance, validated_data):
        validated_data.pop('current_password', None)
        validated_data.pop('confirm_password', None)
        new_password = validated_data.pop('new_password', None)

        for attr, data in validated_data.items():
            setattr(instance, attr, data)

        if new_password:
            instance.set_password(new_password)

        instance.save()
        print(instance)

        return instance

class UserManagementSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False, min_length=4)
    is_active = serializers.BooleanField(required=False)
    is_active = serializers.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['id','username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']

    def update(self, instance, validated_data):
        for attr, data in validated_data.items():
            setattr(instance, attr, data)
        instance.save()
        return instance
