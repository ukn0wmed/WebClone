from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api import C_views 
from api.F_views import categories_products,categories_product_details,products_top_ten

urlpatterns=[
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    
    path('products/',C_views.GenericListCreateProducts.as_view(),name='products'),
    path('products/<int:pk>',C_views.GenericRetrieveProduct.as_view(),name='product'),
    path('products/topten/',products_top_ten,name='Topten'),
    path('products/<int:pk>/comments',C_views.GenericListCreateComments.as_view(),name='product'),

    path('myproducts/',C_views.GenericListCreateMyProducts.as_view(),name="myProducts"),
    path('myproducts/<int:pk>/',C_views.GenericRetrieveUpdateDestroyMyProductDetails.as_view(),name="myProducts"),
    path('myorders/',C_views.GenericListCreateMyOrders.as_view(),name="myOrders"),

    path('categories/<int:pk>/',C_views.GenericRetrieveCategory.as_view(),name='categories_products'),
    path('categories/', C_views.GenericListCategories.as_view(), name='categories'),
   
    path('categories/<int:pk>/products',categories_products,name='categories_products'),
    path('categories/<int:pk>/products/<int:product_id>/',categories_product_details,name='categories_product')
    ]

