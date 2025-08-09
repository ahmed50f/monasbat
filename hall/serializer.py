from rest_framework import serializers
from .models import Hall, Extra_Packges, Basic_Packges


class HallSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(required=False, default=True)
    class Meta:
        model = Hall
        fields = '__all__'

class Extra_PackgesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extra_Packges
        fields = '__all__'

class Basic_PackagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basic_Packges
        fields = '__all__'

    
class PopularHallsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = '__all__'
        filters ={'rate',}