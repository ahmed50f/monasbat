from django.shortcuts import render
from rest_framework import viewsets
from django.utils.translation import gettext_lazy as _
from .models import Light, UserLight
from .serializer import LightSerializer, UserLightSerializer
from accounts.utils import send_notification  


class LightViewSet(viewsets.ModelViewSet):
    queryset = Light.objects.all()
    serializer_class = LightSerializer

    def get_queryset(self):
        return Light.objects.all()

    def perform_create(self, serializer):
        light = serializer.save()

        # ✅ إشعار عند إضافة Light جديد
        send_notification(
            user=self.request.user,
            title=_("Light Created"),
            message=_("Light service for {event} has been added to hall {hall}.").format(
                event=light.event_type,
                hall=light.hall.name
            ),
            notif_type="light",
            sender=self.request.user
        )


class UserLightViewSet(viewsets.ModelViewSet):
    queryset = UserLight.objects.all()   
    serializer_class = UserLightSerializer

    def get_queryset(self):
        return UserLight.objects.all()

    def perform_create(self, serializer):
        user_light = serializer.save()

        # ✅ إشعار عند إضافة UserLight جديد
        send_notification(
            user=self.request.user,
            title=_("User Light Created"),
            message=_("User Light service {name} has been added.").format(
                name=user_light.name
            ),
            notif_type="user_light",
            sender=self.request.user
        )
