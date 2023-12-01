from rest_framework import serializers
from carts.models import OrderItem,Order
from product.models import GoldProductModel

class OrderSeriliazer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.email',read_only=True)
    class Meta:
        model = Order
        fields = ["id","user","order_date","total_price","status"]

class ProductDetailSeriliazer(serializers.ModelSerializer):
    class Meta:
        model = GoldProductModel
        fields = "__all__"
class OrderReportSerializer(serializers.ModelSerializer):
    order = OrderSeriliazer(read_only=True)
    product = ProductDetailSeriliazer(read_only=True)
    class Meta:
        model = OrderItem
        fields = "__all__"