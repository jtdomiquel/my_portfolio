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
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = UserInfoManager()

    USERNAME_FIELD = 'username'  # Field used for authentication
    REQUIRED_FIELDS = []  # Add other required fields here, like email

    def __str__(self):
        return self.username

class portfolio_details(models.Model):
    user_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='user_id')
    project_title = models.CharField(max_length=100, blank=True, null=True)
    thumbnail_image = models.ImageField(upload_to='portfolio_thumbnails/', blank=True, null=True)
    project_discriptions = models.CharField(max_length=500, blank=True, null=True)
    priority = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    skills = models.CharField(max_length=100, blank=True, null=True)
    date_finished = models.DateTimeField(null=True)
    date_save = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

class portfolio_files(models.Model):
    portfolio_id = models.ForeignKey(portfolio_details, on_delete=models.CASCADE, related_name='portfolio_id')
    picture_path = models.ImageField(upload_to='portfolio_files/', blank=True, null=True)
    date_save = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

class portfolio_features(models.Model):
    feature_user_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='feature_user_id')
    feature_portfolio_id = models.ForeignKey(portfolio_details, on_delete=models.CASCADE, related_name='feature_portfolio_id')
    feature_title = models.CharField(max_length=100, blank=True, null=True)
    thumbnail_image = models.ImageField(upload_to='portfolio_feature_thumbnails/', blank=True, null=True)
    feature_discriptions = models.CharField(max_length=500, blank=True, null=True)
    priority = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    skills = models.CharField(max_length=100, blank=True, null=True)
    date_finished = models.DateTimeField(null=True)
    date_save = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

class portfolio_features_files(models.Model):
    portfolio_feat_id = models.ForeignKey(portfolio_features, on_delete=models.CASCADE, related_name='portfolio_feat_id')
    picture_path = models.ImageField(upload_to='portfolio_feature_files/', blank=True, null=True)
    date_save = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
