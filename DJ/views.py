from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from .models import DJ, UserDJ
from .serializer import DJSerializer, UserDJSerializer    
from accounts.utils import send_notification  


class DJViewSet(viewsets.ModelViewSet):
    queryset = DJ.objects.all()
    serializer_class = DJSerializer

    def get_queryset(self):
        return DJ.objects.all()

    def perform_create(self, serializer):
        dj = serializer.save()

        # ✅ إشعار عند إضافة DJ جديد
        send_notification(
            user=self.request.user,
            title=_("DJ Created"),
            message=_("DJ {dj} has been added to hall {hall}.").format(
                dj=dj.dj_name,
                hall=dj.hall.name
            ),
            notif_type="dj",
            sender=self.request.user
        )


class TopDJViewSet(viewsets.ModelViewSet):
    def list(self, request):
        queryset = DJ.objects.all().order_by('-rate')[:5]
        serializer = DJSerializer(queryset, many=True)
        return Response(serializer.data)


class UserDJViewSet(viewsets.ModelViewSet):
    queryset = UserDJ.objects.all()
    serializer_class = UserDJSerializer

    def get_queryset(self):
        return UserDJ.objects.all()

    def perform_create(self, serializer):
        user_dj = serializer.save()

        # ✅ إشعار عند إضافة UserDJ جديد
        send_notification(
            user=self.request.user,
            title=_("User DJ Created"),
            message=_("User DJ {name} has been added.").format(
                name=user_dj.name
            ),
            notif_type="user_dj",
            sender=self.request.user
        )
