from django.db.models import fields
from rest_framework import serializers
from .models import Customer,Comment,User,Data
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from . import google
from .register import generate_username
import os

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model= Comment
        fields=('comment_date','comment_time','customer_id','call_duration','call_status','comment_detail',)

class CustomerSerializer(serializers.ModelSerializer):
    id=serializers.CharField(max_length=255,read_only=True)
    class Meta:
        model=Customer
        fields=('id','firstphone','secondphone','thirdphone','email','location','details','firsttag','secondtag','team','dateadded','first_comment_date','age','due_date_time','label','name',)


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields=('employee_id','date','Talk_Time','Total_Dial','Unique_Dial','Connected_Call','First_Call','Last_Call',' status','Leads_Assigned','Leads_Declined')


class GoogleSocialAuthSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    name = serializers.CharField(max_length=255, min_length=3,write_only=True)
    username= serializers.CharField(max_length=255, min_length=3,read_only=True)
    id= serializers.CharField(max_length=255, min_length=3,read_only=True)


    class Meta:
        model=User
        fields = ['email', 'name']

    def validate(self, attrs):
        email = attrs.get('email', '')
        name = attrs.get('name','')
        provider = 'google'
        filtered_user_by_email = User.objects.filter(email=email)
        if filtered_user_by_email.exists():
            if provider == filtered_user_by_email[0].auth_provider:
                registered_user = User.objects.get(email=email)
                if not registered_user:
                    raise AuthenticationFailed(' user exist but Invalid credentials, try again')
                return {
                    'username': registered_user.username,
                    'email': registered_user.email,
                    'tokens': registered_user.tokens(),
                    'id':registered_user.id,
                    }

            else:
                raise AuthenticationFailed(
                    detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

        else:
            user = {
                'username': generate_username(name), 'email': email,
                'password': 'UggE-791jU6iy947m0sRVmj0'}
            user = User.objects.create_user(**user)
            user.is_verified = True
            user.auth_provider = provider
            user.name= name
            user.save()

            new_user = User.objects.get(email=email)
            if not new_user:
                raise AuthenticationFailed('user created but Invalid credentials, try again')
            return {
                'email': new_user.email,
                'username': 'hehe',
                'tokens': new_user.tokens(),
                'id':new_user.id,
            
            }
            return super().validate(attrs)    
        
    



class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    id= serializers.CharField(read_only=True)
    phone= serializers.CharField()
    position=serializers.CharField()
    working_status =serializers.CharField()
    class Meta:
        model=User
        fields=('name','id','email','phone','position','working_status')