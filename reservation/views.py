from django.shortcuts import render
from django.utils.translation import gettext_lazy as _ 
from rest_framework import viewsets
from .models import Hall, Reservation, Payment
from .serializer import  ReservationSerializers, PaymentSerializers
from django.http import JsonResponse
from django.db import transaction
from datetime import datetime
# Create your views here.

    
class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializers
    def get_queryset(self):
        queryset = Reservation.objects.all()
        return queryset
    
class PaymentViewSet(viewsets.ViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializers
    def get_queryset(self):
        queryset = Payment.objects.all()
        return queryset
    

@transaction.atomic
def book_hall(request, name, date):
    try:
        start_time_str = request.GET.get('start_time')
        end_time_str = request.GET.get('end_time')

        if not start_time_str or not end_time_str:
            return JsonResponse({'error': _('you must enter start time and end time')}, status=400)

        start_time = datetime.strptime(start_time_str, '%H:%M').time()
        end_time = datetime.strptime(end_time_str, '%H:%M').time()
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()

        if start_time >= end_time:
            return JsonResponse({'error': _('the start time must be before the end time')}, status=400)

        hall = Hall.objects.select_for_update().get(name=name)

        # التحقق من وجود تعارض زمني
        conflict_exists = Reservation.objects.filter(
            hall=hall,
            date=date_obj,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exists()

        if conflict_exists:
            return JsonResponse({'error': _('the hall already booked')}, status=400)

        # إنشاء الحجز
        Reservation.objects.create(
            hall=hall,
            user=request.user,
            date=date_obj,
            start_time=start_time,
            end_time=end_time
        )

        return JsonResponse({'message':_('your reservation has been completed successfully')}, status=201)

    except Hall.DoesNotExist:
        return JsonResponse({'error': _('the hall not found')}, status=404)

    except ValueError:
        return JsonResponse({'error': _('Invalid time or date format')}, status=400)
