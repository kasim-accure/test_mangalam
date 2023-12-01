from django.shortcuts import get_object_or_404, render
from rest_framework import generics,views,response,status,mixins
from carts.models import Cart, CartItems,Order,OrderItem,Favorite
from carts import serializers as cart_serializers
from rest_framework import permissions ,serializers
from django.db import transaction
from product.models import GoldProductModel
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist


class CartItemsListCreateView(generics.ListCreateAPIView):
    serializer_class = cart_serializers.CartItemsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItems.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        product_id = serializer.validated_data['product']

        cart_item = CartItems.objects.filter(user=user, product=product_id).first()
        if cart_item:
            error_msg = {"status":False,"message":f"This product ({product_id}) is already in the cart."}
            raise serializers.ValidationError(error_msg)
        cart, created = Cart.objects.get_or_create(user=user, ordered=False)
        serializer.save(user=user, cart=cart)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        if serializer.data:
            response_data = {"success": True,"data": serializer.data}
            return response.Response(response_data,status=status.HTTP_200_OK)
        else:
            response_data = {"success": False,"data": serializer.data}
            return response.Response(response_data,status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        responses = super().create(request, *args, **kwargs)
        response_data = {"success": True,"data": responses.data}
        return response.Response(response_data, status=status.HTTP_201_CREATED)
    
class CartItemsUpdateView(generics.UpdateAPIView):
    queryset = CartItems.objects.all()
    serializer_class = cart_serializers.CartItemsSerializer


    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        serializer = self.get_serializer(queryset, many=True)
        response_data = {"success": True,"data": serializer.data}
        return response.Response(response_data,status=status.HTTP_200_OK)

class CartItemDeleteView(generics.DestroyAPIView):
    queryset = CartItems.objects.all()
    serializer_class = cart_serializers.CartItemsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        cart = instance.cart
        instance.delete()
        total_price = sum(item.price for item in cart.cart_cartitem.all())
        cart.total_price = total_price
        cart.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return response.Response({"success": True, "response": "Cart item deleted successfully"}, status=status.HTTP_200_OK)
    


class ConvertCartToOrderView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    @transaction.atomic
    def post(self, request):
        user = request.user 
        try:
            cart = Cart.objects.get(user=user, ordered=False)
        except ObjectDoesNotExist:
            return response.Response({"status":False,"message":"Cart does not exist"},status=status.HTTP_404_NOT_FOUND)
        
        order = Order.objects.create(user=user, total_price=cart.total_price)
        
        for cart_item in CartItems.objects.filter(cart=cart):
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                price=cart_item.price,
                quantity=cart_item.quantity
            )
            cart_item.delete()
        
        cart.ordered = True
        cart.save()
        cart.delete()
        
        return response.Response({'order_id': order.id}, status=status.HTTP_201_CREATED)


class CheckCartItemsView(generics.ListAPIView):
    serializer_class = cart_serializers.CartItemsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return CartItems.objects.filter(user=self.request.user,product__id=product_id)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        if serializer.data:
            response_data = {"success": True,"message": "Product is already in your cart!"}
            return response.Response(response_data,status=status.HTTP_200_OK)
        else:
            response_data = {"success": False,"data": "Not data found"}
            return response.Response(response_data,status=status.HTTP_404_NOT_FOUND)
        
class AddFavoriteView(generics.CreateAPIView,mixins.CreateModelMixin):
    serializer_class = cart_serializers.AddFavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        
        if not product_id:
            return Response({"success":False,'error': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if Favorite.objects.filter(product=product_id,user=request.user).exists():
            return Response({"success":False,'error': 'Product is already in favorite.'}, status=status.HTTP_400_BAD_REQUEST)


        product = get_object_or_404(GoldProductModel, pk=product_id)
        serializer = self.get_serializer(data={'product': product_id})
        serializer.is_valid(raise_exception=True)
        
        serializer.save(user=request.user, product=product)
        
        return Response({"success":True,'message': 'Product add to Favorite successfully'},status=status.HTTP_200_OK)
    
class FavoriteListView(generics.ListAPIView):
    serializer_class = cart_serializers.FavoriteListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {"success": True,"data": serializer.data}
        return Response(response_data,status=status.HTTP_200_OK)
    

class DeleteFavoriteView(generics.CreateAPIView):
    serializer_class = cart_serializers.AddFavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        
        if not product_id:
            return Response({'error': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(GoldProductModel, pk=product_id)
        favorite = get_object_or_404(Favorite, user=request.user, product=product)

        favorite.delete()

        return Response({"success":True,'message': 'Product remove from Favorite successfully'},status=status.HTTP_200_OK)