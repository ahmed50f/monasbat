from django.shortcuts import render
from .models import DJ, UserDJ
from .serializer import DJSerializer, UserDJSerializer    
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
        queryset = DJ.objects.all().order_by('-rate')[:5]
        serializer = DJSerializer(queryset, many=True)
        return Response(serializer.data)

class UserDJViewSet(viewsets.ModelViewSet):
    queryset = UserDJ.objects.all()
    serializer_class = UserDJSerializer
    def get_queryset(self):
        return UserDJ.objects.all()