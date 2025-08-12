from django.shortcuts import render
from .models import Light, UserLight
from .serializer import LightSerializer, UserLightSerializer
from rest_framework import viewsets
# Create your views here.
class LightViewSet(viewsets.ModelViewSet):
    queryset = Light.objects.all()
    serializer_class = LightSerializer
    def get_queryset(self):
        return Light.objects.all()


class UserLightViewSet(viewsets.ModelViewSet):
    queryset = Light.objects.all()
    serializer_class = UserLightSerializer
    def get_queryset(self):
        return UserLight.objects.all()
