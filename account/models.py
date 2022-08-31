from typing import Callable
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.deletion import CASCADE
from user_profile.models import Profile

role_options = [
    ('Student', 'Student'),
    ('Teacher', 'Teacher'),

]

# upload location for images of the user

def upload_location(instance, filename):
    file_path = 'account/{author_id}/profile_pic_{filename}'.format(
        author_id=str(instance.email), filename=filename)
    return file_path


# creates user - normal user and super user
class MyAccountManager(BaseUserManager):
    def create_user(self, email, first_name, password=None):
        if not email:
            raise ValueError('User must provide a valid email')
        if not first_name:
            raise ValueError('User must provide First Name ')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, password):
        user = self.create_user(
            email=email,
            password=password,
            first_name=first_name,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# account model
class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(max_length=40, choices=role_options, default=role_options[0][0])
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)
    designation = models.CharField(max_length=50, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)

    # USERNAME_FIELD will be what we want to login as email or username
    USERNAME_FIELD = 'email'

    # The fields which must be filled up
    REQUIRED_FIELDS = ['first_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.first_name

    # For checking permissions. to keep it simple all admin have ALL permissions
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        self.designation = str(self.role)
        #Profile.objects.create(user=self)
        saved = super(Account, self).save()




