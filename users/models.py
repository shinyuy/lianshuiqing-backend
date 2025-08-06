from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)
from django.conf import settings
from django.core.mail import send_mail
import uuid
import string
import secrets
# from branch.models import Branch


class UserAccountManager(BaseUserManager):
    def generate_random_password(self, length=10):
        chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(chars) for _ in range(length))
    
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        email = email.lower()
        external_id = uuid.uuid4()

        user = self.model(
            email=email,
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        
        # send_mail('Test',
        #   'This is the message you want to send',
        #   settings.DEFAULT_FROM_EMAIL,
        #   [
        #       email, # add more emails to this list of you want to
        #   ])

        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.create_user(
            email,
            password=password,
            **kwargs
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('waiter', 'Waiter'),
        ('admin', 'Admin/Manager'),
    )
       
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    external_id = models.UUIDField(default=uuid.uuid4, editable=False)
    
      # Add the branch field
    branch = models.ForeignKey('branch.Branch', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')


    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
  
    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
  
  