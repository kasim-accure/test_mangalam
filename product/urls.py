from django.urls import path,include
from product import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r'gold-product-detail', views.GetGoldProductItemDetailView)

app_name = "product"

urlpatterns = [
    path('', include(router.urls)),
    path("category-list/",views.GetCategoryListView.as_view(),name="category-list"),
    path("product-type/<int:category_id>/",views.GetGoldListView.as_view(),name="product-type"),
    path("sub-product-list/<int:product_type_id>/",views.GetGoldSubProductTypeListView.as_view(),name="gold-sub-product-list"),
    path("product-item-list/<int:product_type_id>/",views.ProductItemListView.as_view(),name="product-item-list"),
    path("product-detail/<int:pk>/",views.GetGoldProductItemDetailView.as_view(),name="gold-sub-product-list"),
    path("check-favorite/<int:pk>/",views.CheckIsFavoriteView.as_view(),name="check-favorite"),
    
    
    
    path("gold-product-list/",views.GetGoldProductTypeListView.as_view(),name="gold-product-list"),
    path("latest-product/",views.LatestProductListView.as_view(),name="latest-product"),
    path("latest-product-type/",views.LatestProductTypeListView.as_view(),name="latest-producttype"),
    path("best-selling-product/",views.BestSellerProductListView.as_view(),name="best-selling"),
    
    
]