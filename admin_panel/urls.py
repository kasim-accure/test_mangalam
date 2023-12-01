from django.urls import path
from admin_panel import views

app_name = "admin_panel"

urlpatterns = [
    ########## Dashboard ####################################
    path('dashboard-details/',views.DashboardDetailsApi.as_view(),name="dashboard-details"),
    path("cofirm-order-list/",views.CofirmOrderListView.as_view(),name="confirmorder_list"),
    path("delivered-order-list/",views.DeliveredOrderListView.as_view(),name="deliveredorder_list"),
    path("cancelled-order-list/",views.CancelledOrderListView.as_view(),name="cancelledorder_list"),
    path("decline-order-list/",views.DeclineOrderListView.as_view(),name="declineorder_list"),

    ############# Login Section #################################
    path("login/",views.AdminUserLoginView.as_view(),name="admin_login"),
    path("logout/",views.AdminUserLogout.as_view(),name="admin_logout"),

    ############# User Part #################################
    path("userdetail/",views.AllUserDetailsView.as_view(),name="user_details"),
    path("create-new-user/",views.CreateNewUserView.as_view(),name="create_user"),
    path("<int:pk>/delete-user/",views.DeleteUserView.as_view(),name="delete_user"),

    ############# Category Part #################################
    path("category-list/",views.GetCategoryListView.as_view(),name="category-list"),
    path("create-category/",views.CreateCategoryView.as_view(),name="create-category"),
    path("<int:pk>/update-category/",views.UpdateCategoryView.as_view(),name="update-category"),
    path("<int:pk>/delete-category/",views.DeleteCategoryView.as_view(),name="delete-category"),


    ############# Product Type Part #################################
    path("product-type-list/",views.GetProductTypeListView.as_view(),name="product-type-list"),
    path("create-product-type/",views.CreateProductTypeView.as_view(),name="create-product-type"),
    path("<int:pk>/update-product-type/",views.UpdateProductTypeView.as_view(),name="update-product-type"),
    path("<int:pk>/delete-product-type/",views.DeleteProductTypeView.as_view(),name="delete-product-type"),

    ############# Product Detail Part #################################
    path("product-item-list/",views.ProductItemsListView.as_view(),name="product_item_list"),
    path("add/product-item/",views.CreateNewProductItemsView.as_view(),name="add-product_item"),
    path("update/<int:pk>/product-item/",views.UpdateProductItemAPIView.as_view(),name="update-product_item"),
    path("delete/<int:pk>/product-item/",views.DeleteProductItemView.as_view(),name="delete-product_item"),

    ############# Order Part #################################

    path("approve-order-list/",views.ApprovedCartItemsListView.as_view(),name="to_approve"),
    path("order-to-approve/<int:pk>/",views.OrderToApproveAPIView.as_view(),name="order_to_approve"),
    path("order-list/",views.OrderListView.as_view(),name="order_list"),

    ############# Search #################################
    path("filter-by-category/",views.ListProductTypeListView.as_view(),name="filter-by-category"),

    

    
    
]