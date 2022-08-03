from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response, status

from users.models import User
from users.permissions import IsAdmin, IsOwner
from users.serializers import (LoginSerializer, UpdateStatusSerializer,
                               UserSerializer)


class ListCreateUserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ListNewestUserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):

        num = self.kwargs['num']

        return self.queryset.order_by('-date_joined')[0:num]

class UpdateUserView(generics.UpdateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    queryset = User.objects.all()
    serializer_class = UserSerializer

class UpdateUserStatusView(generics.UpdateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]

    queryset = User.objects.all()
    serializer_class = UpdateStatusSerializer


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )

        if user:
            token = Token.objects.get_or_create(user=user)[0]

            return Response({'token': token.key})

        return Response({"detail": 'invalid email or password'}, status.HTTP_401_UNAUTHORIZED)
        
