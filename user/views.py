from django.shortcuts import render
from rest_framework import generics, status
from .serializers import RegisterSerializer, LoginSerializer, UpdateUserSerializer, AdminRegisterSerializer, UserManagementSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User


# Create your views here.

class UserRegistration(generics.CreateAPIView):

    serializer_class = RegisterSerializer

    def create(self, request):
        serilaizer = RegisterSerializer(data=request.data)

        #is_valid calls the seriallizer's validate method
        serilaizer.is_valid(raise_exception=True)
        serilaizer.save()
        return Response(serilaizer.data, status=status.HTTP_201_CREATED)

class AdminRegistration(generics.CreateAPIView):
    serializer_class = AdminRegisterSerializer

    def validate(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(generics.GenericAPIView):

    serializer_class = LoginSerializer

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TestAuthentication(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data={
            'msg': 'User Authenticated'
        }
        return Response(data, status=status.HTTP_200_OK)

class UserUpdate(generics.RetrieveUpdateAPIView):

    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)

class UserManagementView(generics.RetrieveUpdateDestroyAPIView):

    queryset = User.objects.filter(is_superuser=False)
    serializer_class = UserManagementSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user_id = self.kwargs.get('pk')
        print(user_id)
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

