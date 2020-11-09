from django.db import models
import uuid
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)

from rest_framework_simplejwt.tokens import RefreshToken

class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

    def authenticate(self, username=None, password=None):
        """ Authenticate a user based on email address as the user name. """
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'email': 'email'}


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username=models.CharField(max_length=255,unique=True,db_index=True)
    email = models.EmailField(max_length=254,unique=True)
    is_verified = models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_At= models.DateTimeField(auto_now=True)
    name=models.CharField(max_length=255)
    phone=models.CharField(max_length=100,blank=True,null=True)
    position=models.CharField(max_length=100,blank=True,null=True)
    working_status=models.CharField(max_length=100,blank=True,null=True)
    auth_provider = models.CharField(max_length=255,blank=False,null=False,default=AUTH_PROVIDERS.get('google'))
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects=UserManager()

    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh' : str(refresh),
            'access' : str(refresh.access_token)
        }

class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstphone= models.CharField(max_length=100,blank=True,null=True)
    secondphone= models.CharField(max_length=100,blank=True,null=True)
    thirdphone= models.CharField(max_length=100,blank=True,null=True)
    email= models.CharField(max_length=100,blank=True,null=True)
    name = models.CharField(max_length=100,blank=True,null=True)
    location= models.CharField(max_length=10000,blank=True,null=True)
    details= models.CharField(max_length=20000,blank=True,null=True)
    firsttag= models.CharField(max_length=100,blank=True,null=True)
    secondtag= models.CharField(max_length=100,blank=True,null=True)
    team= models.CharField(max_length=100,blank=True,null=True)
    assignedto_id= models.CharField(max_length=100,blank=True,null=True)
    dateadded= models.DateField(auto_now=False,auto_now_add=False,blank=True,null=True)
    first_comment_date= models.DateField(auto_now=False,auto_now_add=False,blank=True,null=True)
    age = models.IntegerField(blank=True,null=True)
    due_date_time=models.DateTimeField(auto_now=False,auto_now_add=False,blank=True,null=True)
    label=models.CharField(max_length=50,blank=True,null=True)


class Comment(models.Model):
    comment_date=models.DateField(auto_now=False,auto_now_add=False,blank=True,null=True)
    comment_time=models.TimeField(auto_now=False, auto_now_add=False,blank=True,null=True)
    customer_id= models.CharField(max_length=100,blank=True,null=True)
    call_duration = models.CharField(max_length=100,blank=True,null=True)
    call_status=models.CharField(max_length=100,blank=True,null=True)
    comment_detail=models.CharField(max_length=1000,blank=True,null=True)


class Data(models.Model):
    employee_id= models.CharField(max_length=100,blank=True,null=True)
    date=models.DateField(auto_now=False,auto_now_add=False,blank=True,null=True)
    Talk_Time = models.CharField(max_length=100,blank=True,null=True)
    Total_Dial = models.CharField(max_length=100,blank=True,null=True)
    Unique_Dial=models.CharField(max_length=100,blank=True,null=True)
    Connected_Call=models.CharField(max_length=100,blank=True,null=True)
    First_Call=models.CharField(max_length=100,blank=True,null=True)
    Last_Call=models.CharField(max_length=100,blank=True,null=True)
    status=models.CharField(max_length=100,blank=True,null=True)
    Leads_Assigned=models.CharField(max_length=100,blank=True,null=True)
    Leads_Declined=models.CharField(max_length=100,blank=True,null=True)
    



