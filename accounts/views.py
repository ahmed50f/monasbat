from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from fcm_django.models import FCMDevice
from django.utils.translation import gettext as _

from .utils import get_tokens_for_user
from .exceptions import InvalidCredentialsException, UserAlreadyExistsException

User = get_user_model()


@api_view(["POST"])
def register(request):
    phone_number = request.data.get("phone_number")
    password = request.data.get("password")

    if not phone_number or not password:
        return Response({"detail": "Phone number and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(phone_number=phone_number).exists():
        raise UserAlreadyExistsException()

    user = User.objects.create_user(phone_number=phone_number, password=password)
    tokens = get_tokens_for_user(user)

    return Response({
        "user": {"id": user.id, "phone_number": user.phone_number},
        "tokens": tokens,
    }, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def login(request):
    phone_number = request.data.get("phone_number")
    password = request.data.get("password")

    user = authenticate(request, phone_number=phone_number, password=password)
    if not user:
        raise InvalidCredentialsException()

    tokens = get_tokens_for_user(user)

    return Response({
        "user": {"id": user.id, "phone_number": user.phone_number},
        "tokens": tokens,
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    user = request.user
    refresh_token = request.data.get("refresh")

    if refresh_token:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response({"detail": _("Invalid refresh token.")}, status=400)

    # حذف أجهزة FCM المرتبطة
    devices = FCMDevice.objects.filter(user=user)
    if devices.exists():
        devices.delete()

    return Response({"message": _("Logout successful.")})
