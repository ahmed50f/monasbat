from django.shortcuts import render
from .models import Light
from .serializer import LightSerializer
from rest_framework import viewsets
# Create your views here.
class LightViewSet(viewsets.ModelViewSet):
    queryset = Light.objects.all()
    serializer_class = LightSerializer
    def get_queryset(self):
        return Light.objects.all()



