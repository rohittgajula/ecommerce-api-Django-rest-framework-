from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.db import IntegrityError
import uuid


class CustomUserManager(BaseUserManager):
  def create_user(self, email, password, username, **extra_fields):
    if not email:
      raise ValueError("please enter email.")
    if self.model.objects.filter(username=username).exists():
      raise IntegrityError("Username already exixts.")
    if self.model.objects.filter(email=email).exists():
      raise IntegrityError("Email already exists.")
    email = self.normalize_email(email)
    # hashed_password = make_password(password=password)
    user = self.model(email=email, username=username, **extra_fields)
    user.set_password(password)
    user.is_active = True
    user.save()
    return user
  
  def create_superuser(self, email, password, username, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)
    extra_fields.setdefault('is_active', True)

    if not extra_fields.get('is_staff'):
      raise ValueError("is staff must be true.")
    if not extra_fields.get('is_superuser'):
      raise ValueError("is superuser must be true.")

    user = self.create_user(email, password, username, **extra_fields)
    return user


class CustomUser(AbstractBaseUser):
  id = models.AutoField(primary_key=True)
  first_name = models.CharField(max_length=150, blank=False, null=False)
  last_name = models.CharField(max_length=150, blank=False, null=False)
  username = models.CharField(max_length=200, blank=False, null=False)
  email = models.EmailField(max_length=250, unique=True)
  password = models.CharField(max_length=250, blank=False, null=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  reset_password_token = models.CharField(max_length=50, blank=True, default="")
  reset_password_expire = models.DateTimeField(blank=True, null=True)
  is_staff = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

  objects = CustomUserManager()

  def __str__(self):
    return self.username
  
  def has_module_perms(self, app_label):
    return True
  
  def has_perm(self, perm, obj=None):
    return True