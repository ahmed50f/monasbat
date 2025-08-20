from rest_framework import serializers
from .models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from .utils import Util
from django.core.cache import cache
from django.conf import settings
import time
import pyotp
import logging
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from .models import Notification

logger = logging.getLogger(__name__)


    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('phone_number', 'password', 'name', 'email', 'image')
        

    def validate(self, data):
        
        if not (6 <= len(data['password']) <= 16):
            raise serializers.ValidationError({"detail": _("Password must be between 6 and 16 characters.")})
        
        if User.objects.filter(phone_number=data['phone_number']).exists():
            raise serializers.ValidationError({"detail": _("Phone number already exists.")})
        
        email = data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"detail": _("Email already exists.")})
        return data

    def create(self, validated_data):
        #validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user


# Otp Verification Serializer 
class OTPVerificationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        phone = data.get('phone_number')
        otp = data.get('otp')

        if not phone or not otp:
            raise serializers.ValidationError({"detail" : _("Both phone number and OTP are required.")})

        if len(otp) != 4 or not otp.isdigit():
            raise serializers.ValidationError({"detail" : _("Invalid OTP format.")})

        return data
    

# Reset Password Serializer 
class ResetPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        phone_number = data.get('phone_number')
        otp = data.get('otp')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if not phone_number or not otp or not new_password or not confirm_password:
            raise serializers.ValidationError({"detail" : _("All fields are required.")})

        if len(otp) != 4 or not otp.isdigit():
            raise serializers.ValidationError({"detail" : _("Invalid OTP format.")})

        if new_password != confirm_password:
            raise serializers.ValidationError({"detail" : _("Passwords do not match.")})

        return data


# Profile Serializer 
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'phone_number', 'image']
        read_only_fields = ['phone_number']

 
 # User Profile Update Serializer 
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'phone_number', 'email', 'image']  # Define fields to update
        read_only_fields = ['phone_number']



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = self.context['request'].user

        if not user.check_password(data['old_password']):
            raise serializers.ValidationError({"old_password": _("Old password is incorrect.")})

        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": _("New passwords do not match.")})

        if len(data['new_password']) < 6 or len(data['new_password']) > 16:
            raise serializers.ValidationError({"new_password": _("Password must be between 6 and 16 characters.")})

        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        token_str = attrs.get("refresh")
        self.token = None

        if token_str:
            try:
                self.token = RefreshToken(token_str)
            except Exception:
                raise ValidationError({"refresh": _("Invalid or expired refresh token.")})

        return attrs

    def save(self, **kwargs):
        if self.token:
            try:
                self.token.blacklist()
            except Exception:
                raise ValidationError({"refresh": _("Token already blacklisted or invalid.")})


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'sender']