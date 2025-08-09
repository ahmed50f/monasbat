from django.shortcuts import render
from rest_framework import viewsets
from .serializer import MusicalBandSerializer
from .models import Musical_Band
from rest_framework.response import Response
# Create your views here.
class Musical_BandViewSet(viewsets.ModelViewSet):
    queryset = Musical_Band.objects.all()
    serializer_class =  MusicalBandSerializer 
    def get_queryset(self):
        return Musical_Band.objects.all()
    
class TopBandViewSet(viewsets.ModelViewSet):
    def list(self, request):
        halls = Musical_Band.objects.order_by('-rate')[:5]  
        serializer = MusicalBandSerializer(Musical_Band, many=True)
        return Response(serializer.data)
