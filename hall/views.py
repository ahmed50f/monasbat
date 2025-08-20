from django.shortcuts import render
from .serializer import HallSerializer, Extra_PackgesSerializer, Basic_PackagesSerializer, UserHallSerializer
from .models import Hall, Extra_Packges, Basic_Packges, UserHall
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from accounts.utils import send_notification

from rest_framework.response import Response
# Create your views here.

class HallViewSet(viewsets.ModelViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    def get_queryset(self):
        queryset = Hall.objects.all()
        return queryset
    
    def perform_create(self, serializer):
        hall = serializer.save()  # يحفظ الهول
        # ابعت إشعار بعد الإنشاء
        send_notification(
            user=self.request.user,       # المستلم
            sender=self.request.user,     # المرسل
            title="New Hall Created",
            message=f"Hall {hall.name} has been created successfully.",
            type="hall"
        )
    
class Extra_PackagesViewSet(viewsets.ModelViewSet):
    queryset = Extra_Packges.objects.all()
    serializer_class = Extra_PackgesSerializer
    def get_queryset(self):
        queryset = Extra_Packges.objects.all()
        return queryset
    
class Basic_PackagesViewSet(viewsets.ModelViewSet): 
    queryset = Basic_Packges.objects.all()
    serializer_class = Basic_PackagesSerializer
    def get_queryset(self):
        queryset = Basic_Packges.objects.all()
        return queryset
    
    def get_list(self):
        queryset = Basic_Packges.objects.all()
        serializer = Basic_PackagesSerializer(queryset, many=True)
        return serializer.data
    

class PopularHallsViewSet(viewsets.ViewSet):
    def list(self, request):
        halls = Hall.objects.order_by('-rate')[:5]  
        serializer = HallSerializer(halls, many=True)
        return Response(serializer.data)

class UserHallViewSet(viewsets.ModelViewSet):
    queryset = UserHall.objects.all()
    serializer_class = UserHallSerializer
    def get_queryset(self):
        queryset = UserHall.objects.all()
        return queryset
    
    def perform_create(self, serializer):
        user_hall = serializer.save()
        send_notification(
            user=self.request.user,
            sender=self.request.user,
            title="New User Hall Added",
            message=f"User hall {user_hall.name} has been added.",
            type="hall"
        )

