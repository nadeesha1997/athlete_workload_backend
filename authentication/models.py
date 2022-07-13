# import jwt
# from datetime import datetime,timedelta
# from django.conf import settings
# from django.contrib.auth.models import (AbstractBaseUser,BaseUserManager,PermissionsMixin)
# from django.db import models

# class UserManager(BaseUserManager):    
#     def create_user(self,username,email,password=None):
#         if username is None:
#             raise TypeError('User must have username')

#         if email is None:
#             raise TypeError('User must have email')
        
#         user=self.model(username=username,email=self.normalize_email(email))
#         user.set_password(password)
#         user.save()
#         return user

#     def create_superuser(self,username,email,password):
#         if password is None:
#             raise TypeError('Superuser should have password')
#         user=self.create_user(username,email,password)
#         user.is_superuser=True
#         user.is_staff=True
#         user.save()
#         return user

# class User(AbstractBaseUser,PermissionsMixin):
#     username=models.CharField(db_index=True,max_length=255,unique=True)
#     email=models.EmailField(db_index=True,unique=True)
#     is_active=models.BooleanField(default=True)
#     is_staff=models.BooleanField(default=False)
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)
#     USERNAME_FIELD='email'
#     REQUIRED_FIELDS = ['username']
#     objects=UserManager()

#     def __str__(self):
#         return self.email

#     @property
#     def token(self):
#         return self._generate_jwt_token()

#     def get_full_name(self):
#         return self.username

#     def get_short_name(self):
#         return self.username

#     def _generate_jwt_token(self):
#         dt=datetime.now()+timedelta(days=60)
#         token=jwt.encode({
#             'id':self.pk,
#             'exp': dt.utcfromtimestamp(dt.timestamp())
#         },settings.SECRET_KEY,algorithm='HS256')
#         return token
        
from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, email, name,tc, password=None,password2=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            tc=tc,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name,tc, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            tc=tc,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=50, default='user')
    tc=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','tc']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin