from django.shortcuts import render
from rest_framework import generics, status
from .serializers import RegisterSerializer
from rest_framework.response import Response

# Create your views here.

class UserRegistration(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serilaizer = RegisterSerializer(data=user)

        #is_valid calls the seriallizer's validate method
        if serilaizer.is_valid():
            serilaizer.save() #'save' calls the serializer's create method
            return Response(serilaizer.data, status=status.HTTP_201_CREATED)

        return Response(serilaizer._errors, status=status.HTTP_400_BAD_REQUEST)