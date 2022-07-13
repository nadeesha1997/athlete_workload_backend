# from dataclasses import fields
# from rest_framework import serializers
# from .models import User

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=User
#         fields=['id','username','name','email','password']
#         extra_kwargs={
#             'password':{'write_only':True}
#         }

#         def create(self,validated_data):
#             password=validated_data.pop('password',None)
#             instance=self.Meta.model(**validated_data)
#             if password is not None:
#                 instance.set_password(password)
#             instance.save()
#             return instance
#########################################################################################
# from rest_framework import serializers
# from .models import User
# from django.contrib.auth import authenticate

# class RegistrationSerializer(serializers.ModelSerializer):
#     password=serializers.CharField(
#         max_length=128,
#         min_length=8,
#         write_only=True
#     )
#     token=serializers.CharField(max_length=255,read_only=True)
#     class Meta:
#         model=User
#         fields = ['email', 'username', 'password', 'token']
    
#     def create(self, validated_data):
#         return User.objects.create_user(**validated_data)


# class LoginSerializer(serializers.Serializer):
#     email=serializers.CharField(max_length=255)
#     username=serializers.CharField(max_length=255, read_only=True)
#     password=serializers.CharField(max_length=128,write_only=True)
#     token=serializers.CharField(max_length=255,read_only=True)

#     def validate(self, data):
#         email=data.get('email',None)
#         password=data.get('password',None)
#         if email is None:
#             raise serializers.ValidationError('An email address is required to login')
#         if password is None:
#             raise serializers.ValidationError('A password is required to login')
#         user=authenticate(username=email, password=password)
#         if user is None:
#             raise serializers.ValidationError('A user with this email and password was not found.')
#         if not user.is_active:
#             raise serializers.ValidationError('This user has been deactivated.')
#         return {
#             'email':user.email,
#             'username':user.username,
#             'token':user.token
#         }


# class UserSerializer(serializers.ModelSerializer):
#     password=serializers.CharField(max_length=128,min_length=8,write_only=True)

#     class Meta:
#         model=User
#         fields=('email','username','password','token')
#         read_only_fields=('token',)

#     def update(self, instance, validated_data):
#         password=validated_data.pop('password',None)
#         for (key,value) in validated_data.items():
#             setattr(instance,key,value)

#         if password is not None:
#             instance.set_password(password)
#         instance.save()
#         return instance
#####################################################################################################
from rest_framework import serializers
from .models import User
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['email','name','password','password2','tc']
        extra_kwargs={
            'password':{'write_only':True}
        }
    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        if password !=password2:
            raise serializers.ValidationError("Password and confirm password doesnt match")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=User
        fields=['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','name']

class UserChangePasswordSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['password','password2']
    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        if password !=password2:
            raise serializers.ValidationError("Password and confirm password doesnt match")
        user=self.context.get('user')
        user.set_password(password)
        user.save()
        return attrs

class SendResetPasswordEmailSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=User
        fields=['email']
    def validate(self, attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            link='http://127.0.0.1/auth/reset/'+uid+'/'+token
            print(link)
            return attrs
        else:
            raise serializers.ValidationError('You are not a registered user')