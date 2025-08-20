from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _

from .serializer import MusicalBandSerializer, UserMusicalBandSerializer
from .models import Musical_Band, UserMusical_Band
from accounts.utils import send_notification


class Musical_BandViewSet(viewsets.ModelViewSet):
    queryset = Musical_Band.objects.all()
    serializer_class = MusicalBandSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        band = serializer.save()

        # ✅ إرسال إشعار بعد إضافة فرقة موسيقية
        send_notification(
            user=self.request.user,
            title=_("Band Created"),
            message=_("Band {band} has been added to hall {hall}.").format(
                band=band.name,
                hall=band.hall.name
            ),
            notif_type="musical_band",
            sender=self.request.user
        )


class TopBandViewSet(viewsets.ReadOnlyModelViewSet):  # ✅ للتصفح فقط
    queryset = Musical_Band.objects.all()
    serializer_class = MusicalBandSerializer

    def list(self, request, *args, **kwargs):
        halls = Musical_Band.objects.order_by('-rate')[:5]
        serializer = self.get_serializer(halls, many=True)
        return Response(serializer.data)


class UserMusicalBandViewSet(viewsets.ModelViewSet):
    queryset = UserMusical_Band.objects.all()
    serializer_class = UserMusicalBandSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        band = serializer.save(user=self.request.user, status="pending")

        # ✅ إرسال إشعار بعد إضافة الباند من اليوزر
        send_notification(
            user=self.request.user,
            title=_("New Band Added"),
            message=_("You have successfully added your band {band_name}.").format(
                band_name=band.name
            ),
            notif_type="user_musical_band",
            sender=self.request.user
        )
