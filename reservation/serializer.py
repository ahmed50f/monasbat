from rest_framework import serializers
from .models import Reservation, Payment


class ReservationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        field = '__all__'

class PaymentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Payment
        field = '__all__'

