from django.urls import path
from . import views


urlpatterns = [
    path('allproducts/', views.product_list.as_view(), name='product-list'),
    path('product/<slug:slug>/', views.product_detail.as_view(), name='product_details'),
    path('categories/', views.category_list.as_view(), name='category_list'),
    path('category/<slug:slug>', views.category_detailed.as_view(), name='category_details'),
]