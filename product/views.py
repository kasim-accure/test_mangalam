from django.shortcuts import render
from product import serializers as product_serializer
from rest_framework import generics,mixins,viewsets,response,status,views
from rest_framework.response import Response 
from product.models import GoldProductModel,Category,ProductTypeModel
from rest_framework.permissions import IsAuthenticated
from collections import defaultdict
from carts.models import OrderItem
from django.db.models import Sum,Count


class GetCategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = product_serializer.CategoryListSerializer
    permission_classes = [IsAuthenticated]
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {"success": True,"data": serializer.data}
        return response.Response(response_data,status=status.HTTP_200_OK)

class ProductItemListView(generics.ListAPIView):
    queryset = GoldProductModel.objects.all()
    serializer_class = product_serializer.GoldProductItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product_type_id = self.kwargs['product_type_id']
        model = self.request.query_params.get("model",None)
        queryset = GoldProductModel.objects.filter(product_type__id=product_type_id)
        

        if model:
            queryset = queryset.filter(model=model)
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        if serializer.data:
            # data = serializer.data

            # grouped_data = defaultdict(list)

            # for item in data:
            #     sub_model = item.get('sub_model')
            #     grouped_data[sub_model].append(item)

            response_data = {"success": True,"data": serializer.data}
        
        else:
            response_data = {"success": False,"data": "Not data found"}
        # response_data = {"success": True,"data": serializer.data}
        return response.Response(response_data,status=status.HTTP_200_OK)


class GetGoldProductTypeListView(generics.ListAPIView):
    queryset = GoldProductModel.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = GoldProductModel.objects.values("product_type").distinct()
        return Response(queryset)

class GetGoldSubProductTypeListView(generics.ListAPIView):
    queryset = GoldProductModel.objects.all()
    serializer_class = product_serializer.GetGoldSubProductTypeListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product_type_id = self.kwargs['product_type_id']
        # product_type_id = self.request.query_params.get("product_type",None)
        queryset = GoldProductModel.objects.filter(product_type__id=product_type_id).values("model").distinct()
        

        # if product_type:
        #     product_type = product_type.lower()
        #     queryset = queryset.filter(product_type__product_type__iexact=product_type).values("model").distinct()
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        if serializer.data:
            # for item in serializer.data:
            #     if item['model'] is None:
            #         response_data = {"success": False,"data": "Not data found"}
            #     else:
            response_data = {"success": True,"data": serializer.data}
        else:
            response_data = {"success": False,"data": "Not data found"}
        return response.Response(response_data,status=status.HTTP_200_OK)


class GetGoldProductItemDetailView(generics.ListAPIView):
    queryset = GoldProductModel.objects.all()
    serializer_class = product_serializer.GoldProductItemSerializer
    permission_classes = [IsAuthenticated]

    
    def get_queryset(self):
        product_item_id = self.kwargs['pk']
        queryset = GoldProductModel.objects.filter(id=product_item_id)
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        if serializer.data:
            response_data = {"success": True,"data": serializer.data}
        else:
            response_data = {"success": False,"data": "Not data found"}
        
        return Response(response_data, status=status.HTTP_200_OK)


class GetGoldListView(generics.ListAPIView):
    queryset = ProductTypeModel.objects.all()
    serializer_class = product_serializer.GetProductTypeListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        querset = ProductTypeModel.objects.filter(category__id=category_id)            #.values("image","product_type").distinct()
        return querset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        # response_data = {"success": True,"data": serializer.data}
        if serializer.data:
            response_data = {"success": True,"data": serializer.data}
        else:
            response_data = {"success": False,"data": "Not data found"}
        return response.Response(response_data,status=status.HTTP_200_OK)


class CheckIsFavoriteView(generics.ListAPIView):
    queryset = GoldProductModel.objects.all()
    serializer_class = product_serializer.CheckIsFavoriteSerializer
    permission_classes = [IsAuthenticated]

    
    def get_queryset(self):
        product_item_id = self.kwargs['pk']
        queryset = GoldProductModel.objects.filter(id=product_item_id)
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        if serializer.data:
            response_data = {"success": True,"data": serializer.data}
        else:
            response_data = {"success": False,"data": "Not data found"}
        
        return Response(response_data, status=status.HTTP_200_OK)


class LatestProductListView(generics.ListAPIView):
    queryset = GoldProductModel.objects.all()
    serializer_class = product_serializer.GoldProductItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        querset = GoldProductModel.objects.order_by('-created')[:5]
        return querset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        if serializer.data:
            response_data = {"success": True,"data": serializer.data}
        else:
            response_data = {"success": False,"data": "Not data found"}
        return response.Response(response_data,status=status.HTTP_200_OK)

class LatestProductTypeListView(generics.ListAPIView):
    queryset = ProductTypeModel.objects.all()
    serializer_class = product_serializer.GetProductTypeListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        querset = ProductTypeModel.objects.order_by('-created')[:10]
        return querset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        if serializer.data:
            response_data = {"success": True,"data": serializer.data}
        else:
            response_data = {"success": False,"data": "Not data found"}
        return response.Response(response_data,status=status.HTTP_200_OK)

class BestSellerProductListView(views.APIView):
    serializer_class = product_serializer.BestSellerSerializer

    def get_top_5_most_ordered_products(self):
        # Aggregate data to get the top 5 most ordered products
        top_5_most_ordered_products = OrderItem.objects.values(
            'product__id', 'product__product_name'
        ).annotate(total_orders=Count('id')).order_by('-total_orders')[:2]
        return top_5_most_ordered_products

    def get(self, request):
        top_5_most_ordered_products = self.get_top_5_most_ordered_products()
        
        # Fetch the actual Product instances using the IDs obtained
        product_ids = [item['product__id'] for item in top_5_most_ordered_products]
        top_products = GoldProductModel.objects.filter(id__in=product_ids)
        print(top_products,"---Product")
        
        serializer = self.serializer_class(top_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)