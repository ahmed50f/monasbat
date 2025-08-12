# views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem, UserDJ, UserMusicalBand, UserLight
from .serializers import (CartItemSerializer, UserDJSerializer,
                          UserMusicalBandSerializer, UserLightSerializer)

class UserDJViewSet(viewsets.ModelViewSet):
    queryset = UserDJ.objects.all()
    serializer_class = UserDJSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status='pending')

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:  # الأدمن يشوف الكل
            return UserDJ.objects.all().order_by('-created_at')
        return UserDJ.objects.filter(user=user).order_by('-created_at')

class UserMusicalBandViewSet(viewsets.ModelViewSet):
    queryset = UserMusicalBand.objects.all()
    serializer_class = UserMusicalBandSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status='pending')

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return UserMusicalBand.objects.all().order_by('-created_at')
        return UserMusicalBand.objects.filter(user=user).order_by('-created_at')

class UserLightViewSet(viewsets.ModelViewSet):
    queryset = UserLight.objects.all()
    serializer_class = UserLightSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status='pending')

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return UserLight.objects.all().order_by('-created_at')
        return UserLight.objects.filter(user=user).order_by('-created_at')

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user).order_by('-added_at')

