from django.shortcuts import render
from admin_panel import serializers as adminpanel_serializer
from rest_framework import generics,mixins,viewsets,response,status,views
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated
from admin_panel.permissions import IsAdminUser
from users.models import User
from product.models import Category,ProductTypeModel,GoldProductModel,ProductImages
from carts.models import CartItems ,OrderItem
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from django.db.models import Q





class AdminUserLoginView(views.APIView):

    def post(self,request,*args, **kwargs):
        data = request.data
        username = data.get('username',None)
        password = data.get('password',None)

        if not username or not password:
            return Response({'success':False, 'data':{}, 'message':'Provide username or password'},status=status.HTTP_400_BAD_REQUEST)
        
        user = None


        if username.isnumeric():
            user = User.objects.filter(mobile=username).first()
        else:
            user = User.objects.filter(email__iexact=username).first()
        
        if not user:
            return Response({'success':False, 'data':{}, 'message':'Invalid credentials! '},status=status.HTTP_403_FORBIDDEN)
        
        
        if not user.is_admin:
            return Response({'success':False, 'data':{}, 'message':'You do not have permission to perform this action!'},status=status.HTTP_403_FORBIDDEN)

        if user.check_password(password):
            if user.is_active:
                resp = {
                    'user_id': user.id,
                    'first_name' : user.first_name,
                    'last_name' : user.last_name,
                    'mobile' : user.mobile,
                    'email' : user.email,
                    'city' : user.city,
                    'state' : user.state,
                    'country':user.country,
                    'zipcode' : user.zipcode,
                    'address_1':user.address_1,'address_2':user.address_2,
                    'active' : user.is_active,
                    'auth_token': self.get_auth_token(user)
                }
                return Response({'success':True, 'data':resp, 'message':'Successfully Logged In! '},status=status.HTTP_200_OK)
            else:
                return Response({'success':False, 'data':{}, 'message':'Account deactivated! Contant Admin.'},status=status.HTTP_403_FORBIDDEN)
            
        return Response({'success':False, 'data':{}, 'message':'Invalid credentials! , Check username or password '},status=status.HTTP_403_FORBIDDEN)
    

    def get_auth_token(self, user:User) ->dict:
        token, created = Token.objects.get_or_create(user=user)
        token_reponse = {
            'token' : str(token.key),
        }
        return token_reponse


class DashboardDetailsApi(views.APIView):
    # permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            all_user = User.objects.all().count()
            new_order = OrderItem.objects.filter(status="pending").count()
            confirm_order = OrderItem.objects.filter(status="approved").count()
            decline_order = OrderItem.objects.filter(status="decline").count()
            delivered_order = OrderItem.objects.filter(status="delivered").count()
            cancelled_order = OrderItem.objects.filter(status="cancelled").count()
            
            return Response(data={"status": True, "all_users":all_user,"new_orders":new_order,"confirm_order":confirm_order,
                                  "decline_order":decline_order,"delivered_order":delivered_order,"cancelled_order":cancelled_order}, status=status.HTTP_200_OK)
    
        except Exception as e:
            return Response(data={"status": False, 'vehicle': str(e)}, status=status.HTTP_400_BAD_REQUEST)
 
class CofirmOrderListView(generics.ListCreateAPIView):
    serializer_class = adminpanel_serializer.OrderListSeriliazer

    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return OrderItem.objects.filter(status="approved")
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {"success": True,"data": serializer.data}
        return Response(response_data,status=status.HTTP_200_OK)

class DeliveredOrderListView(generics.ListCreateAPIView):
    serializer_class = adminpanel_serializer.OrderListSeriliazer

    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return OrderItem.objects.filter(status="delivered")
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {"success": True,"data": serializer.data}
        return Response(response_data,status=status.HTTP_200_OK)
class CancelledOrderListView(generics.ListCreateAPIView):
    serializer_class = adminpanel_serializer.OrderListSeriliazer

    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return OrderItem.objects.filter(status="cancelled")
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {"success": True,"data": serializer.data}
        return Response(response_data,status=status.HTTP_200_OK)
class DeclineOrderListView(generics.ListCreateAPIView):
    serializer_class = adminpanel_serializer.OrderListSeriliazer

    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return OrderItem.objects.filter(status="decline")
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {"success": True,"data": serializer.data}
        return Response(response_data,status=status.HTTP_200_OK)
class AdminUserLogout(views.APIView):
    permission_classes = [IsAdminUser]

    def post(self,request,*args, **kwargs):
        logout(request)
        return Response({"success":True,"message":"You have been successfully logged out"},status=200)
  
class AllUserDetailsView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = adminpanel_serializer.AllUserDetailSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        search = self.request.query_params.get('search',None)
        queryset = User.objects.all()

        if search:
            queryset = queryset.filter( Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(email=search)| Q(mobile__icontains=search))          
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {"success": True,"data": serializer.data}
        return Response(response_data,status=status.HTTP_200_OK)

class CreateNewUserView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = adminpanel_serializer.UserRegisterSerializer
    permission_classes = [IsAdminUser]

    def get_serializer_context(self):
        return {
            "request":self.request,
            "args" : self.args,
            "kwargs" : self.kwargs
        }
class DeleteUserView(mixins.RetrieveModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = adminpanel_serializer.AllUserDetailSerializer
    permission_classes = [IsAdminUser,]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"success": True,'message': 'Record deleted successfully.'},status=status.HTTP_200_OK)
class UserDeleteAPIView(mixins.DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = adminpanel_serializer.UserDeleteSerializer
    permission_classes = [IsAdminUser]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"success": True,'message': 'Record deleted successfully.'},status=status.HTTP_200_OK)
        

class GetCategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = adminpanel_serializer.GetCategoryListSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        search = self.request.query_params.get('search',None)
        queryset = Category.objects.all()

        if search:
            queryset = queryset.filter(category_name__icontains=search)          
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {"success": True,"data": serializer.data}
        return Response(response_data,status=status.HTTP_200_OK)
    


class CreateCategoryView(generics.CreateAPIView,mixins.CreateModelMixin,mixins.UpdateModelMixin):

    queryset = Category.objects.all()
    serializer_class = adminpanel_serializer.GetCategoryListSerializer
    permission_classes = [IsAdminUser]

    def get_serializer_context(self, *args, **kwargs):
        return {
            "request": self.request,
            "args": self.args,
            "kwargs": self.kwargs
        }
class UpdateCategoryView(generics.UpdateAPIView,mixins.RetrieveModelMixin):
    queryset = Category.objects.all()
    serializer_class = adminpanel_serializer.GetCategoryListSerializer
    permission_classes = [IsAdminUser,]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class DeleteCategoryView(mixins.RetrieveModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = adminpanel_serializer.GetCategoryListSerializer
    permission_classes = [IsAdminUser,]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"success": True,'message': 'Record deleted successfully.'},status=status.HTTP_200_OK)

class GetProductTypeListView(generics.ListAPIView):
    queryset = ProductTypeModel.objects.all()
    serializer_class = adminpanel_serializer.ProductTypeListSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        search = self.request.query_params.get('search',None)
        queryset = ProductTypeModel.objects.all()

        if search:
            queryset = queryset.filter(Q(category__category_name__icontains=search) | Q(product_type__icontains=search))       
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {"success": True,"data": serializer.data}
        return Response(response_data,status=status.HTTP_200_OK)


class CreateProductTypeView(generics.CreateAPIView,mixins.CreateModelMixin,mixins.UpdateModelMixin):

    queryset = ProductTypeModel.objects.all()
    serializer_class = adminpanel_serializer.ProductTypeCreateSerializer
    permission_classes = [IsAdminUser]

    def get_serializer_context(self, *args, **kwargs):
        return {
            "request": self.request,
            "args": self.args,
            "kwargs": self.kwargs
        }

class UpdateProductTypeView(generics.UpdateAPIView,mixins.RetrieveModelMixin):
    queryset = ProductTypeModel.objects.all()
    serializer_class = adminpanel_serializer.ProductTypeCreateSerializer
    permission_classes = [IsAdminUser,]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class DeleteProductTypeView(mixins.RetrieveModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = ProductTypeModel.objects.all()
    serializer_class = adminpanel_serializer.ProductTypeCreateSerializer
    permission_classes = [IsAdminUser,]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return response.Response({"success": True,'message': 'Record deleted successfully.'},status=status.HTTP_200_OK)

class ApprovedCartItemsListView(generics.ListAPIView):
    serializer_class = adminpanel_serializer.OrderListSeriliazer

    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return OrderItem.objects.filter(status="pending")
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {"success": True,"data": serializer.data}
        return Response(response_data,status=status.HTTP_200_OK)


class ProductItemsListView(generics.ListCreateAPIView):
    serializer_class = adminpanel_serializer.ProductDetailSeriliazer

    permission_classes = [IsAdminUser]

    def get_queryset(self):
        search = self.request.query_params.get('search',None)
        queryset = GoldProductModel.objects.all()

        if search:
            queryset = queryset.filter(Q(category__category_name__icontains=search) | Q(product_type__product_type__icontains=search)
                                       | Q(product_id__icontains=search) | Q(product_name__icontains=search)| Q(hu_id__icontains=search))       
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {"success": True,"data": serializer.data}
        return Response(response_data,status=status.HTTP_200_OK)


class CreateNewProductItemsView(generics.CreateAPIView,mixins.CreateModelMixin,mixins.UpdateModelMixin):

    queryset = GoldProductModel.objects.all()
    serializer_class = adminpanel_serializer.ProductItemCreateSeriliazer
    permission_classes = [IsAdminUser]

    def get_serializer_context(self):
        return {
            "request":self.request,
            "args" : self.args,
            "kwargs" : self.kwargs
        }
    def perform_create(self, serializer):
        # Save the product details
        product_instance = serializer.save()

        # Get the uploaded images from the request
        images_datas = self.request.FILES.getlist('images', [])
        for image_data in images_datas:
            # Create an entry for each image uploaded for the product
            ProductImages.objects.create(product=product_instance, images=image_data)

        return Response({"success": True,'message': 'Product created succesfully.'},status=status.HTTP_201_CREATED)
class UpdateProductItemAPIView(generics.UpdateAPIView,mixins.RetrieveModelMixin):
    queryset = GoldProductModel.objects.all()
    serializer_class = adminpanel_serializer.ProductItemCreateSeriliazer
    permission_classes = [IsAdminUser,]

    def perform_update(self, serializer):
        product_instance = serializer.save()
        images_datas = self.request.FILES.getlist('images', [])

        # Delete old images associated with the product
        ProductImages.objects.filter(product=product_instance).delete()

        # Create entries for each new image uploaded for the product
        for image_data in images_datas:
            ProductImages.objects.create(product=product_instance, images=image_data)

        return Response({"success": True, 'message': 'Product updated successfully.'}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class DeleteProductItemView(mixins.RetrieveModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = GoldProductModel.objects.all()
    serializer_class = adminpanel_serializer.ProductItemCreateSeriliazer
    permission_classes = [IsAdminUser,]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"success": True,'message': 'Record deleted successfully.'},status=status.HTTP_200_OK)
    


class OrderListView(generics.ListCreateAPIView):
    serializer_class = adminpanel_serializer.OrderListSeriliazer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return OrderItem.objects.filter(status="approved")
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {"success": True,"data": serializer.data}
        return Response(response_data,status=status.HTTP_200_OK)


class OrderToApproveAPIView(generics.UpdateAPIView,mixins.RetrieveModelMixin):
    queryset = OrderItem.objects.all()
    serializer_class = adminpanel_serializer.OrderToApproveSeriliazer
    permission_classes = [IsAdminUser,]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ListProductTypeListView(generics.ListAPIView):
    queryset = ProductTypeModel.objects.all()
    serializer_class = adminpanel_serializer.FilterProductTypeListSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        category_name = self.request.query_params.get("category",None)
        queryset = ProductTypeModel.objects.filter(category__category_name=category_name)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {"success": True,"data": serializer.data}
        return response.Response(response_data,status=status.HTTP_200_OK)