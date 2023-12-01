from django.urls import path
from users import views

app_name = "users"

urlpatterns = [
    # path("user-register/",views.UserRegisterView.as_view(),name='user_register'),
    path("user-login/",views.UserLoginView.as_view(),name="user-login"),
    path("user-logout/",views.UserLogout.as_view(),name="user-logout"),
    path("user-profile/",views.GetUserProfileAPIView.as_view(),name="user-profile"),
    path('update/user-profile/',views.UserProfileUpdateView.as_view(),name="update-profile"),
    path('edit/user-address/',views.UserAddressUpdateView.as_view(),name="update-address"),
]