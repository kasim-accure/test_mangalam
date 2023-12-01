from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from users.managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):


    first_name = models.CharField(max_length=255,blank=True,null=True)
    last_name = models.CharField(max_length=255,blank=True,null=True)
    email = models.EmailField(max_length=255,unique=True,blank=True,null=True)
    mobile = models.CharField(max_length=20,unique=True,blank=True,null=True)
    zipcode = models.CharField(max_length=20,blank=True,null=True)
    city = models.CharField(max_length=100,blank=True,null=True)
    state = models.CharField(max_length=100,blank=True,null=True)
    country = models.CharField(max_length=100,blank=True,null=True)
    address_1 = models.CharField(max_length=255,blank=True,null=True)
    address_2 = models.CharField(max_length=255,blank=True,null=True)
    house_or_building = models.CharField(max_length=275, null=True, blank=True)
    road_or_area = models.CharField(max_length=275, null=True, blank=True)
    landmark = models.CharField(max_length=275, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()

    def __str__(self):
        return f"{self.email}"
