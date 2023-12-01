from rest_framework import serializers
from product.models import GoldProductModel,Category, ProductTypeModel,ProductImages
from carts.models import Favorite,OrderItem



class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
class GetProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ["images"]
class GoldProductItemSerializer(serializers.ModelSerializer):
    product_images = GetProductImagesSerializer(many=True, source='product_images.all' ,read_only=True)
    is_favorite = serializers.SerializerMethodField()
    class Meta:
        model = GoldProductModel
        fields = "__all__"
    def get_is_favorite(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            # Check if the product is in the user's favorites
            return Favorite.objects.filter(product=obj, user=user).exists()
        return False

class GetGoldSubProductTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoldProductModel
        fields = ["id","model"]

class GetProductTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTypeModel
        fields = ["id","product_type","image"]


class CheckIsFavoriteSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()
    class Meta:
        model = GoldProductModel
        fields = ["id","is_favorite"]
    def get_is_favorite(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            # Check if the product is in the user's favorites
            return Favorite.objects.filter(product=obj, user=user).exists()
        return False

class BestSellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoldProductModel
        fields = "__all__"