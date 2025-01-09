from django.shortcuts import render
from rest_framework import generics, status
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny


# Create your views here.

class UserRegistration(generics.CreateAPIView):

    serializer_class = RegisterSerializer

    def create(self, request):
        serilaizer = RegisterSerializer(data=request.data)

        #is_valid calls the seriallizer's validate method
        serilaizer.is_valid(raise_exception=True)
        serilaizer.save()
        return Response(serilaizer.data, status=status.HTTP_201_CREATED)

class UserLogin(generics.GenericAPIView):

    serializer_class = LoginSerializer

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token = serializer.validated_data.get('access_token')
        response =  Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        response['Authorization'] = f"Bearer {access_token}"

        return response

class TestAuthentication(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data={
            'msg': 'User Authenticated'
        }
        return Response(data, status=status.HTTP_200_OK)