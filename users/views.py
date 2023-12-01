from django.shortcuts import render
from users.models import User
from rest_framework import generics,views,status,mixins,response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from users import serializers as user_serializers
from rest_framework.authtoken.models import Token




class UserLoginView(views.APIView):

    def post(self,request,*args, **kwargs):
        data = request.data
        username = data.get('username',None)
        password = data.get('password',None)

        if not username or not password:
            return response.Response({'success':False, 'data':{}, 'message':'Provide username or password'},status=status.HTTP_400_BAD_REQUEST)
        
        user = None


        if username.isnumeric():
            user = User.objects.filter(mobile=username).first()
        else:
            user = User.objects.filter(email__iexact=username).first()
        
        if not user:
            return response.Response({'success':False, 'data':{}, 'message':'Invalid credentials! '},status=status.HTTP_403_FORBIDDEN)
        
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
                return response.Response({'success':True, 'data':resp, 'message':'Successfully Logged In! '},status=status.HTTP_200_OK)
            else:
                return response.Response({'success':False, 'data':{}, 'message':'Account deactivated! Contant Admin.'},status=status.HTTP_403_FORBIDDEN)
            
        return response.Response({'success':False, 'data':{}, 'message':'Invalid credentials! , Check username or password '},status=status.HTTP_403_FORBIDDEN)
    

    def get_auth_token(self, user:User) ->dict:
        # auth_token = RefreshToken.for_user(user)

        # token = {
        #     'access' : str(auth_token.access_token),
        #     'refresh' : str(auth_token)
        # }
        token, created = Token.objects.get_or_create(user=user)
        token_reponse = {
            'token' : str(token.key),
        }
        return token_reponse


class UserLogout(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,*args, **kwargs):
        logout(request)
        return response.Response({"success":True,"message":"You have been successfully logged out"},status=200)
    
class GetUserProfileAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = user_serializers.GetUserProfileSerializer
    permission_classes = [IsAuthenticated,]

    def get_object(self):
        return self.request.user


class UserProfileUpdateView(views.APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = user_serializers.UserProfileUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response({"success":True,"data":serializer.data},status=status.HTTP_202_ACCEPTED)
        return response.Response(serializer.errors, status=400)


class UserAddressUpdateView(views.APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = user_serializers.UserAddressUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response({"success":True,"data":serializer.data},status=status.HTTP_202_ACCEPTED)
        return response.Response(serializer.errors, status=400)