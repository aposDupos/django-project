import logging

from rest_framework.serializers import ModelSerializer, IntegerField
from .models import Order, Product, Provider, User


class ProviderSerializer(ModelSerializer):
    class Meta:
        model = Provider
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    provider_data = ProviderSerializer(source='provider')

    class Meta:
        model = Product
        exclude = ['provider', ]


class OrderSerializer(ModelSerializer):
    sum = IntegerField(source='get_total_price')
    products = ProductSerializer(source='product', many=True)

    class Meta:
        model = Order
        exclude = ['product', ]

    # def create(self, validated_data):
    #     order = Order.objects.create(**validated_data)
    #     return order


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }