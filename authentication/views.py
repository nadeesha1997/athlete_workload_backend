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
# 
# 
# 
# ###############################################################################################

# from rest_framework import status
# from rest_framework.permissions import AllowAny,IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from authentication.models import User

# from .serializers import (RegistrationSerializer,LoginSerializer,UserSerializer)
# from .renderers import UserJSONRenderer
# from rest_framework.generics import RetrieveUpdateAPIView

# class RegistrationAPIView(APIView):
#     permission_classes=(AllowAny,)
#     renderer_classes=(UserJSONRenderer,)
#     serializer_class=RegistrationSerializer

#     def post(self,request):
#         user=request.data
#         print(user)
#         serializer=self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(serializer.data,status=status.HTTP_201_CREATED)


# class LoginAPIView(APIView):
#     permission_classes=(AllowAny,)
#     renderer_classes=(UserJSONRenderer,)
#     serializer_class=LoginSerializer

#     def post(self,request):
#         user=request.data
#         serializer=self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)


# class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
#     permission_classes=(IsAuthenticated,)
#     renderer_classes=(UserJSONRenderer,)
#     serializer_class=UserSerializer

#     def retrieve(self, request, *args, **kwargs):
#         serializer=self.serializer_class(request.user)
#         return Response(serializer.data,status=status.HTTP_200_OK)

#     def update(self, request, *args, **kwargs):
        # serializer_data=request.data.get('user',{})
        # serializer=self.serializer_class(request.user,data=serializer_data,partial=True)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # return Response(serializer.data,status=status.HTTP_200_OK)
####################################################################################################################
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from authentication.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from authentication.serializers import UserLoginSerializer, UserProfileSerializer, UserRegistrationSerializer

def get_token_for_user(user):
    refresh=RefreshToken.for_user(user)
    # return {
    #     # 'refresh':str(refresh),
    #     'access':str(refresh.access_token),
    # }
    return str(refresh.access_token)

class UserRegistrationView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token=get_token_for_user(user)
            return Response({'token':token,'msg':'registration success'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self,request,format=None):
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                token=get_token_for_user(user)
                return Response({'token':token,'msg':'Login Success','name':user.name},status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_fiels_errors':['Email or password invakid']}},status=status.HTTP_401_UNAUTHORIZED)

class UserProfileView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        serializer=UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
        # return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# class UserChangePasswordView(APIView):
#     renderer_classes=[UserRenderer]
#     permission_classes=[IsAuthenticated]
#     def post(self,request,format=None):
#         serializer=UserChangePasswordSerializer(data=request.data,context={'user':request.user})
#         if serializer.is_valid(raise_exception=True):
#             return Response({'msg':'Password change Success'},status=status.HTTP_200_OK)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# class SendResetPasswordEmailView(APIView):
#     renderer_classes=[UserRenderer]
#     permission_classes=[IsAuthenticated]
#     def post(self,request,format=None):
#         serializer=SendResetPasswordEmailSerializer(data=request.data)
#         if serializer.is_valid():
#             return Response({'msg':'Reset password link sent.Check your email'},status=status.HTTP_200_OK)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)