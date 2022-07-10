# from django.db import models
# from django.contrib.auth.models import AbstractUser

# # Create your models here.
# class User(AbstractUser):
#     name=models.CharField(max_length=50)
#     email=models.CharField(max_length=100, unique=True)
#     password=models.CharField(max_length=100)
#     username=models.CharField(max_length=100, unique=True)

#     USERNAME_FIELD: 'email'
#     REQUIRED_FIELDS: []

import jwt
from datetime import datetime,timedelta
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser,BaseUserManager,PermissionsMixin)
from django.db import models

class UserManager(BaseUserManager):    
    def create_user(self,username,email,password=None):
        if username is None:
            raise TypeError('User must have username')

        if email is None:
            raise TypeError('User must have email')
        
        user=self.model(username=username,email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,username,email,password):
        if password is None:
            raise TypeError('Superuser should have password')
        user=self.create_user(username,email,password)
        user.is_superuser=True
        user.is_staff=True
        user.save()
        return user

class User(AbstractBaseUser,PermissionsMixin):
    username=models.CharField(db_index=True,max_length=255,unique=True)
    email=models.EmailField(db_index=True,unique=True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['username']
    objects=UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        dt=datetime.now()+timedelta(days=60)
        token=jwt.encode({
            'id':self.pk,
            'exp': dt.utcfromtimestamp(dt.timestamp())
        },settings.SECRET_KEY,algorithm='HS256')
        return token
        