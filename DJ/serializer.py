from rest_framework import serializers
from .models import DJ

class DJSerializer(serializers.ModelSerializer):
    class Meta:
        model = DJ
        fields = '__all__'

class TopDJSerializer(serializers.ModelSerializer):
    class Meta:
        model = DJ
        fields = '__all__'
        filter = {'rate',}