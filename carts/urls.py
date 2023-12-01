from django.urls import path,include
from carts import views


app_name = "carts"

urlpatterns = [ 
    # path('carts/', views.CartListCreateView.as_view(), name='cart-list-create'),
    path('cartitems/', views.CartItemsListCreateView.as_view(), name='cartitems-list-create'),
    path('cartitems/<int:pk>/update/', views.CartItemsUpdateView.as_view(), name='cartitems-update'),
    path('cartitems/<int:pk>/delete/', views.CartItemDeleteView.as_view(), name='cartitems-delete'), 

    path('check-cartitem/<int:product_id>/', views.CheckCartItemsView.as_view(), name='cartitems-check'), 
    path('add-to-favorite/', views.AddFavoriteView.as_view(), name='add_favorite'),
    path('list-favorite/', views.FavoriteListView.as_view(), name='list_favorite'),
    path('remove-favorite/', views.DeleteFavoriteView.as_view(), name='remove_favorite'),

    path('order/', views.ConvertCartToOrderView.as_view(), name='order'), 
]