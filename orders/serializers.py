from product.models import GoldProductModel
from carts.models import Cart,OrderItem
from rest_framework import serializers


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoldProductModel
        fields = "__all__"

class OrderItemSerializer(serializers.ModelSerializer):
    product_details = ProductListSerializer(source='product',read_only=True)
    class Meta:
        model = OrderItem
    
        fields = "__all__"