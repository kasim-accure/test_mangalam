from rest_framework import serializers
from users.models import User



class GetUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","first_name","last_name","email","mobile","city","state","country","zipcode","address_1",
                  "address_2","house_or_building","road_or_area","landmark","is_active"]
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','mobile']

class UserAddressUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['zipcode','city','state','country','address_1','address_2','house_or_building','road_or_area','landmark']