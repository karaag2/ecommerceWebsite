from django.urls import path
from . import views


urlpatterns = [
    path('allproducts/', views.ProductList.as_view(), name='product-list'),
    path('product/<slug:slug>/', views.ProductDetail.as_view(), name='product_details'),
    path('categories/', views.CategoryList.as_view(), name='category_list'),
    path('category/<slug:slug>', views.CategoryDetailed.as_view(), name='category_details'),
    path('cart/add/', views.AddToCartView.as_view(), name='cart-add'),
    path('cart/items/<int:pk>/', views.CartItemDetailView.as_view(), name='cart-item-detail'),
    path('cart/updateItem/', views.UpdateCartItemAlternativeView.as_view(), name='cart-item-update'),
    path('cart/<int:pk>/', views.CartDetailView.as_view(), name='cart-detail'),
]