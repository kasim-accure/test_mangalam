from django.urls import path,include
from orders import views
app_name = "orders"

urlpatterns = [
    path("orderitem-list/",views.orderItemsListView.as_view(),name=" orderItemsListView"),
    path("orderitem-search/",views.OrderItemSearchView.as_view(),name=" orderItemsListView"),
    
]