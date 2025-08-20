from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _
from .models import Cart, CartItem, UserDJ, UserMusicalBand, UserLight
from .serializers import (CartItemSerializer, UserDJSerializer,
                          UserMusicalBandSerializer, UserLightSerializer)
from accounts.utils import send_notification  


class UserDJViewSet(viewsets.ModelViewSet):
    queryset = UserDJ.objects.all()
    serializer_class = UserDJSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user_dj = serializer.save(user=self.request.user, status='pending')

        # ✅ إشعار عند إضافة UserDJ
        send_notification(
            user=self.request.user,
            title=_("User DJ Created"),
            message=_("Your DJ request '{name}' has been submitted and is pending approval.").format(
                name=user_dj.name
            ),
            notif_type="user_dj",
            sender=self.request.user
        )

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:  
            return UserDJ.objects.all().order_by('-created_at')
        return UserDJ.objects.filter(user=user).order_by('-created_at')


class UserMusicalBandViewSet(viewsets.ModelViewSet):
    queryset = UserMusicalBand.objects.all()
    serializer_class = UserMusicalBandSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user_band = serializer.save(user=self.request.user, status='pending')

        # ✅ إشعار عند إضافة UserMusicalBand
        send_notification(
            user=self.request.user,
            title=_("User Musical Band Created"),
            message=_("Your Musical Band request '{name}' has been submitted and is pending approval.").format(
                name=user_band.name
            ),
            notif_type="user_band",
            sender=self.request.user
        )

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
        user_light = serializer.save(user=self.request.user, status='pending')

        # ✅ إشعار عند إضافة UserLight
        send_notification(
            user=self.request.user,
            title=_("User Light Created"),
            message=_("Your Light request '{name}' has been submitted and is pending approval.").format(
                name=user_light.name
            ),
            notif_type="user_light",
            sender=self.request.user
        )

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return UserLight.objects.all().order_by('-created_at')
        return UserLight.objects.filter(user=user).order_by('-created_at')


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        cart_item = serializer.save()

        # ✅ إشعار عند إضافة عنصر للسلة
        send_notification(
            user=self.request.user,
            title=_("Cart Updated"),
            message=_("Item '{item}' has been added to your cart.").format(
                item=cart_item.item_name if hasattr(cart_item, 'item_name') else cart_item.id
            ),
            notif_type="cart_item",
            sender=self.request.user
        )

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user).order_by('-added_at')

