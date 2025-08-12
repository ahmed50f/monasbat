from rest_framework import serializers
from .models import Light, UserLight

class LightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Light
        fields = '__all__'

class UserLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLight
        fields = '__all__'