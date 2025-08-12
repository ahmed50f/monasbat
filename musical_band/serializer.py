from rest_framework import serializers
from .models import Musical_Band, UserMusical_Band

class MusicalBandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Musical_Band
        fields = '__all__'

class TopMusicalBandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Musical_Band
        fields = '__all__'
        
class UserMusicalBandSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMusical_Band
        fields = '__all__'