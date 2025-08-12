from rest_framework import serializers
from .models import DJ, UserDJ

class DJSerializer(serializers.ModelSerializer):
    class Meta:
        model = DJ
        fields = '__all__'

class TopDJSerializer(serializers.ModelSerializer):
    class Meta:
        model = DJ
        fields = '__all__'
        
class UserDJSerializer(serializers.ModelSerializer):
    class Meta:
        model = DJ
        fields = '__all__'