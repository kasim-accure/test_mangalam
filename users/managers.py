from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.db.models import Q



class UserQuerySet(models.query.QuerySet):
    def is_current(self):
        return self.filter(Q(is_current=True))
    
    def filter_user(self, user):
        return self.filter(Q(user=user))
    
    def users(self):
        return self.filter(Q(is_superuser=False) & Q(is_admin=False))
    


class UserManager(BaseUserManager):
    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)
    
    def users(self):
        return self.get_queryset().users()
    
    def create_user(self,mobile=None,email=None,first_name=None, last_name=None,password=None, is_active=True,is_staff=False,is_admin=False, is_superuser=False):

        if not email:
            raise ValueError("User must have an email address")
        if not password:
            raise ValueError("User must have a password")
        
        user_obj = self.model(
            mobile=mobile,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        user_obj.set_password(password)
        user_obj.is_staff= is_staff
        user_obj.is_admin = is_admin
        user_obj.is_active = is_active
        user_obj.is_superuser = is_superuser
        user_obj.save(using=self._db)
        return user_obj
    
    def create_new_user(self,mobile=None,email=None,first_name=None, last_name=None,
                        zipcode=None,city=None,state=None,country=None,address_1=None,address_2=None
                        ,password=None, is_active=True,is_staff=False,is_admin=False):
        
        if not email:
            raise ValueError("User must have an email address")
        if not password:
            raise ValueError("User must have a password")
        
        user_obj = self.model(
            mobile=mobile,
            first_name=first_name,
            last_name=last_name,
            email=email,
            zipcode=zipcode,
            city=city,
            state=state,
            country=country,
            address_1=address_1,
            address_2=address_2
        )

        user_obj.set_password(password)
        user_obj.is_staff= is_staff
        user_obj.is_admin = is_admin
        user_obj.is_active = is_active
        
        
        user_obj.save(using=self._db)
        return user_obj
    
    def register_new_user(
        self,mobile=None,email=None,first_name=None, last_name=None,password=None, is_active=True,is_staff=False,is_admin=False):
        
        
        if not email:
            raise ValueError("User must have an email address")
        if not password:
            raise ValueError("User must have a password")
        

        user_obj = self.model(
            mobile=mobile,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        user_obj.set_password(password)
        user_obj.is_staff= is_staff
        user_obj.is_admin = is_admin
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj
    
    def create_staff_user(self,mobile=None,email=None,first_name=None, last_name=None,password=None):

        user = self.create_user(
            mobile=mobile,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_staff=True
        )

        return user
    
    def create_superuser(self,mobile=None,email=None,first_name=None, last_name=None,password=None):
        
        
        user = self.create_user(
            mobile=mobile,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_staff=True,
            is_admin=True,
            is_superuser=True,
        )

        return user
    
    def get_user_by_mobile(self,mobile):
        qs = self.get_queryset().filter(mobile=mobile)

        if qs.exists():
            user_obj = qs.exists()

            return user_obj
    
    def get_or_create_new_user(self, fields):
        mobile = fields.get('mobile')
        user_obj = self.get_user_by_mobile(mobile)

        if user_obj:
            return user_obj,False

        else:
            user_obj = self.create_new_user(**fields)
            return user_obj, True 