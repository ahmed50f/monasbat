import time 
from django.db import transaction
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext as _
from django.utils.crypto import get_random_string
from django.core.cache import cache
from django.conf import settings 
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView 
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from fcm_django.models import FCMDevice
from .serializers import RegisterSerializer, LogoutSerializer, UserProfileUpdateSerializer, OTPVerificationSerializer, ResetPasswordSerializer, ProfileSerializer, ChangePasswordSerializer
from .utils import Util
from rest_framework.permissions import AllowAny
User = get_user_model()


# Register User View
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = serializer.save()
                    phone_number = user.phone_number
                    Util.send_sms_verification(user, phone_number= phone_number)
                    
                    data = {
                        'user': serializer.data,
                        'message': _('User registered successfully, OTP has been sent to your phone number.'),
                    }
                    
                    return Response(data, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                return Response({
                    "detail": _("Registration failed."),
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login 
@api_view(['POST'])
def login(request):
    phone_number = request.data.get("phone_number")
    password = request.data.get("password")
        
    try:
        user = User.objects.get(phone_number=phone_number)
        
        if not user.is_active:
            return Response({"detail": _("Account is not active. Please verify your phone number.")}, status=status.HTTP_403_FORBIDDEN)

        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': _('Login Successfully'),
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id,
                'phone': user.phone_number,
            }, status=status.HTTP_200_OK)
        else:
            return Response({"detail": _("Invalid credentials.")}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({"detail": _("User not found.")}, status=status.HTTP_404_NOT_FOUND)


# Forgot Password
@csrf_exempt
@api_view(['POST'])
def forgot_password(request):
    phone_number = request.data.get("phone_number")

    if not phone_number:
        return Response({"detail": _("Phone number is required.")}, status=400)

    try:
        user = User.objects.get(phone_number=phone_number)
    except User.DoesNotExist:
        return Response({"detail": _("User not found.")}, status=404)

    # Number of OTP resend attempts for password reset
    reset_attempts = cache.get(f"forgot_password_attempts_{phone_number}", 0)

    # Determine wait time based on previous attempts
    wait_time = settings.WAIT_TIMES[min(reset_attempts, len(settings.WAIT_TIMES) - 1)]

    last_sent_time = cache.get(f"forgot_password_last_sent_{phone_number}")
    current_time = time.time()

    if last_sent_time and (current_time - last_sent_time) < wait_time:
        remaining_time = int(wait_time - (current_time - last_sent_time))
        return Response({
            "detail": _(f"Please wait {remaining_time} seconds before requesting a new OTP."),
            "wait_time": remaining_time  # Remaining wait time
        }, status=429)

    # Generate new OTP
    new_otp = get_random_string(length=4, allowed_chars='0123456789')

    # Store OTP in cache for 5 minutes
    cache.set(f"forgot_password_otp_{phone_number}", new_otp, timeout=settings.OTP_TIMEOUT)

    # Update last sent time
    cache.set(f"forgot_password_last_sent_{phone_number}", current_time, timeout=wait_time)

    # Increment OTP resend attempts
    cache.set(f"forgot_password_attempts_{phone_number}", reset_attempts + 1, timeout=86400)  # Reset after 24 hours

    # Send OTP via SMS
    sms_response =  Util.send_sms_verification(user, phone_number=phone_number, otp=new_otp)

    if sms_response:
        return Response({
            "message": _("OTP sent for password reset."),
            "wait_time": wait_time  # Time to wait before requesting a new OTP
        }, status=200)
    else:
        return Response({
            "detail": _("Failed to send OTP. Please try again later."),
            "wait_time": wait_time  # Return wait time even in case of failure
        }, status=500)
    
    

# Verify Forget Password OTP 
@csrf_exempt
@api_view(['POST'])
def verify_forgot_password_otp(request):
    phone_number = request.data.get("phone_number")
    otp = request.data.get("otp")

    if not phone_number or not otp:
        return Response({"detail": _("Phone and OTP are required.")}, status=400)

    stored_otp = cache.get(f"forgot_password_otp_{phone_number}")
    print(stored_otp)

    if stored_otp and otp == stored_otp:
        return Response({"message": _("OTP verified. You can reset your password.")}, status=200)
    else:
        return Response({"detail": _("Invalid or expired OTP.")}, status=400)


# Verify OTP for User Registration      
@csrf_exempt
@api_view(['POST'])
def verify_otp(request):
    serializer = OTPVerificationSerializer(data=request.data)
    if serializer.is_valid():
        phone_number = serializer.validated_data['phone_number']        
        entered_otp = serializer.validated_data['otp']
        stored_otp = cache.get(f"otp_{phone_number}")

        if stored_otp and entered_otp == stored_otp:
            try:
                user = User.objects.get(phone_number=phone_number)
                user.is_active = True
                user.save() 
                cache.delete(f"otp_{phone_number}")  # Delete the OTP from cache 
                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)

                return Response({"message": _("OTP verified. Account activated."), 
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"detail": _("User not found.")}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": _("Invalid OTP.")}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Reset Password View 
@csrf_exempt
@api_view(['POST'])
def reset_password(request):
    serializer = ResetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        phone_number = serializer.validated_data['phone_number']
        entered_otp = serializer.validated_data['otp']
        new_password = serializer.validated_data['new_password']
        stored_otp = cache.get(f"forgot_password_otp_{phone_number}")

        if stored_otp and entered_otp == stored_otp:
            try:
                user = User.objects.get(phone_number=phone_number)
                user.set_password(new_password)
                user.save()
                cache.delete(f"otp_{phone_number}")  # Delete the OTP from cache
                
                return Response({"message": _("Password reset successful.")}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"detail": _("User not found.")}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": _("Invalid OTP.")}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Profile View
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


# Change Password View 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({"message": _("Password changed successfully.")}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Logout View 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    user = request.user
    serializer = LogoutSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()

    devices = FCMDevice.objects.filter(user=user)
    deleted_devices = []
    if devices.exists():
        deleted_devices = [
            {
                'device_id': device.device_id,
                'registration_token': device.registration_id,
                'type': device.type,
            } for device in devices
        ]
        devices.delete()

    return Response({
        "message": _("Logout successfully."),
        "deleted_devices": deleted_devices
    }, status=status.HTTP_200_OK)