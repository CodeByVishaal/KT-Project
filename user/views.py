from django.shortcuts import render
from rest_framework import generics, status
from .serializers import RegisterSerializer
from rest_framework.response import Response

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

    def post(self, request):
        user = request.data