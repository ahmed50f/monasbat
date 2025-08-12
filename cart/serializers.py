# serializers.py
from rest_framework import serializers
from .models import Cart, CartItem, UserDJ, UserMusicalBand, UserLight

class UserDJSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDJ
        fields = '__all__'
        read_only_fields = ('user','status','created_at','updated_at')

class UserMusicalBandSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMusicalBand
        fields = '__all__'
        read_only_fields = ('user','status','created_at','updated_at')

class UserLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLight
        fields = '__all__'
        read_only_fields = ('user','status','created_at','updated_at')

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'
        read_only_fields = ('cart','added_at')

    def validate(self, data):
        item_fields = ['dj','user_dj','musical_band','user_musical_band','light','user_light','hall','reservation']
        provided = [f for f in item_fields if data.get(f) is not None]
        if len(provided) == 0:
            raise serializers.ValidationError("You must provide exactly one item to add to cart.")
        if len(provided) > 1:
            raise serializers.ValidationError("Provide only one item per cart item.")
        return data

    def create(self, validated_data):
        request = self.context['request']
        cart, _ = Cart.objects.get_or_create(user=request.user)
        validated_data['cart'] = cart
        return super().create(validated_data)
