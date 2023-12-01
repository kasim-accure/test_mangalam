from rest_framework import serializers
from users.models import User
from product.models import Category,ProductTypeModel,GoldProductModel
from carts.models import CartItems,OrderItem,Order


class AllUserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id","first_name","last_name","email","mobile","city","state","country","zipcode","address_1",
                  "address_2","is_active"]

class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserRegisterSerializer(serializers.ModelSerializer):

    message = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'first_name','last_name','mobile','email','city','state','country','zipcode','address_1','address_2',
            'password','message'
        ]

        extra_kwargs = {'password' : {'write_only':True}}

    def get_message(self, obj):
        return "Thank you for registering. Please verify your mobile number before continuing."
    
    def validate_mobile(self, value):
        qs = User.objects.filter(mobile=value)

        if qs.exists():
            raise serializers.ValidationError("User with this mobile number already registered.")
        return value
    
    def create(self, validated_data):
        user_obj = User.objects.create_new_user(**validated_data, is_active=True)

        return user_obj


class GetCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class ProductTypeListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.category_name', read_only=True)
    class Meta:
        model = ProductTypeModel
        fields = "__all__"

class ProductTypeCreateSerializer(serializers.ModelSerializer):
    category = serializers.CharField(write_only=True)
    class Meta:
        model = ProductTypeModel
        fields = "__all__"
      
    def create(self, validated_data):
            category = validated_data.pop('category')
            category_obj = Category.objects.filter(category_name=category).first()
            product_type = ProductTypeModel.objects.create(category=category_obj,**validated_data)
            return product_type
    def update(self, instance, validated_data):
        category = validated_data.pop('category', None)
        if category:
            category_obj, created = Category.objects.get_or_create(category_name=category)
            instance.category = category_obj

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
class ProductDetailSeriliazer(serializers.ModelSerializer):
    class Meta:
        model = GoldProductModel
        fields = "__all__"


class ApprovedCartItemsListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.email', read_only=True)
    product = ProductDetailSeriliazer(read_only=True)
    class Meta:
        model = CartItems
        fields = "__all__"

class ProductItemCreateSeriliazer(serializers.ModelSerializer):
    category = serializers.CharField(write_only=True)
    product_type = serializers.CharField(write_only=True)
    class Meta:
        model = GoldProductModel
        fields = "__all__"
        
    def create(self, validated_data):
        category_value = validated_data.pop('category')
        product_type = validated_data.pop('product_type')
        category_obj = Category.objects.filter(category_name=category_value).first()
        product_type_obj = ProductTypeModel.objects.filter(product_type=product_type,category=category_obj).first()
        if  not product_type_obj:
            raise serializers.ValidationError("This Product type should be Category instance!")
        product_item = GoldProductModel.objects.create(category=category_obj,product_type=product_type_obj,**validated_data)
        return product_item
    def update(self, instance, validated_data):
        category_value = validated_data.pop('category')
        product_type = validated_data.pop('product_type')
        
               
        if category_value:
            category_obj = Category.objects.filter(category_name=category_value).first()
            if not category_obj:
                raise serializers.ValidationError("Invalid Category provided!")

            instance.category = category_obj

        if product_type:
            product_type_obj = ProductTypeModel.objects.filter(product_type=product_type, category=instance.category).first()
            if not product_type_obj:
                raise serializers.ValidationError("This Product type should be Category instance!")

            instance.product_type = product_type_obj

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

class OrderSeriliazer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.email',read_only=True)
    class Meta:
        model = Order
        fields = ["id","user","order_date","total_price","status"]
class OrderListSeriliazer(serializers.ModelSerializer):
    order = OrderSeriliazer(read_only=True)
    product = ProductDetailSeriliazer(read_only=True)
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderToApproveSeriliazer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id","status"]


class FilterProductTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTypeModel
        fields = ["product_type"]