from rest_framework import serializers
from carts.models import Cart, CartItems , Favorite
from product.models import GoldProductModel


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.category_name', read_only=True)
    class Meta:
        model = GoldProductModel
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemsSerializer(serializers.ModelSerializer):
    cart_details = CartSerializer(source='cart' ,read_only=True)
    product_details = ProductListSerializer(source='product' ,read_only=True)
    class Meta:
        model = CartItems
        fields = '__all__'

class AddFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'

class FavoriteListSerializer(serializers.ModelSerializer):
    product_details = ProductListSerializer(source='product' ,read_only=True)
    class Meta:
        model = Favorite
        fields = ["id","user","product_details"]