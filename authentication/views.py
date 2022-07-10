# from django.shortcuts import render
# from requests import request
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.exceptions import AuthenticationFailed
# from authentication.models import User
# from rest_framework import generics
# import jwt,datetime
# from . import serializers

# from authentication.serializers import UserSerializer

# # Create your views here.
# class UserView(APIView):
#     def post(self,request):
#         serializer=UserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

# class LoginView(APIView):
#     # data=request.data
#     # serializer_class=serializers.UserSerializer
#     def post(self,request):
#         email=request.data['email']
#         password=request.data['password']

#         user=User.objects.filter(email=email).first()
#         print(user)

#         if user is None:
#             raise AuthenticationFailed('User not found')
#         if not user.check_password(password):
#             raise AuthenticationFailed('Incorrect password')

#         payload={
#             'id':user.id,
#             'exp':datetime.datetime.utcnow+datetime.timedelta(minutes=60),
#             'iat':datetime.datetime.utcnow()
#         }
#         token=jwt.encode(payload,'secret',algorithm='HS256').decode('utf-8')

#         return Response({
#             'jwt':token
#         })
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User

from .serializers import (RegistrationSerializer,LoginSerializer)
from .renderers import UserJSONRenderer

class RegistrationAPIView(APIView):
    permission_classes=(AllowAny,)
    renderer_classes=(UserJSONRenderer,)
    serializer_class=RegistrationSerializer

    def post(self,request):
        user=request.data
        print(user)
        serializer=self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data,status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes=(AllowAny,)
    renderer_classes=(UserJSONRenderer,)
    serializer_class=LoginSerializer

    def post(self,request):
        user=request.data
        serializer=self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_200_OK)