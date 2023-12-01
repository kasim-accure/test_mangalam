from django.shortcuts import render
# from admin_panel import serializers as adminpanel_serializer
# from admin_panel.permissions import IsAdminUserOrReadOnly
from rest_framework.response import Response
from admin_panel.permissions import IsAdminUser
from product.models import GoldProductModel
from carts.models import OrderItem
from rest_framework import generics,status
from orders import serializers

class orderItemsListView(generics.ListAPIView):
    serializer_class = serializers.OrderItemSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return OrderItem.objects.all()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {"success": True,"data": serializer.data}
        return Response(response_data,status=status.HTTP_200_OK)

class OrderItemSearchView(generics.ListAPIView):
    serializer_class = serializers.OrderItemSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = OrderItem.objects.all()
        search_param = self.request.query_params.get('search', None) 
        if search_param:
            queryset = OrderItem.objects.filter(product__product_name__icontains=search_param)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {"success": True, "data": serializer.data}
        return Response(response_data, status=status.HTTP_200_OK)


