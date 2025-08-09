from django.shortcuts import render
from .models import DJ
from .serializer import DJSerializer    
from rest_framework import viewsets
from rest_framework.response import Response
# Create your views here.
class DJViewSet(viewsets.ModelViewSet):
    queryset =DJ.objects.all()
    serializer_class = DJSerializer
    def get_queryset(self):
        return DJ.objects.all()

class TopDJViewSet(viewsets.ModelViewSet):
    def list(self, request):
        queryset =DJ.objects.all().order_by('-rating')[:5]
        serializer_class = DJSerializer(DJ , many=True)
        return Response(DJ.data)