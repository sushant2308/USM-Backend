from django.db.models import fields
from rest_framework import serializers
from .models import Customer,Comment,User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from . import google
from .register import register_social_user
import os

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model= Comment
        fields=('comment_date','comment_time','customer_id','call_duration','call_status','comment_detail',)

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields=('id','firstphone','secondphone','thirdphone','email','location','details','firsttag','secondtag','team','dateadded','first_comment_date','age','due_date_time','label')





class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        if user_data['aud'] != os.environ.get('GOOGLE_CLIENT_ID'):

            raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name)



class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    id= serializers.CharField(read_only=True)
    class Meta:
        model=User
        fields=('name','id','email','phone','position','working_status')