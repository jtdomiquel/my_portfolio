from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
# Create your models here.

class UserInfoManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        """Create and return a regular user with a username and password"""
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)  # Hash password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """Create and return a superuser with a username and password"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)

# Custom user model
class UserInfo(AbstractBaseUser, PermissionsMixin):
    firstname = models.CharField(max_length=100, blank=True, null=True)
    middlename = models.CharField(max_length=50, blank=True, null=True)
    lastname = models.CharField(max_length=100, blank=True, null=True)
    contact_no = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128) 
    user_type = models.CharField(max_length=100, blank=True, null=True)
    office_name = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = UserInfoManager()

    USERNAME_FIELD = 'username'  # Field used for authentication
    REQUIRED_FIELDS = []  # Add other required fields here, like email

    def __str__(self):
        return self.username
