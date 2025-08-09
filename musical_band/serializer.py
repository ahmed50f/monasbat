from rest_framework import serializers
from .models import Musical_Band

class MusicalBandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Musical_Band
        fields = '__all__ '

class TopMusicalBandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Musical_Band
        fields = '__all__'
        filter = {'rate'}