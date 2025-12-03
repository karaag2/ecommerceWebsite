from django.urls import path
from . import views


urlpatterns = [
    path('allproducts/', views.ProductList.as_view(), name='product-list'),
    path('product/<slug:slug>/', views.ProductDetail.as_view(), name='product_details'),
    path('categories/', views.CategoryList.as_view(), name='category_list'),
    path('category/<slug:slug>', views.CategoryDetailed.as_view(), name='category_details'),
    path('cart/add/', views.AddToCartView.as_view(), name='cart-add'),
    # path('cart/items/<int:pk>/', views.CartItemDetailView.as_view(), name='cart-item-detail'),
    path('cart/delete/<int:pk>/', views.DeleteCartItemView.as_view(), name='cart-item-delete'),
    path('cart/updateItem/<int:pk>/', views.UpdateCartItemAlternativeView.as_view(), name='cart-item-update'),
    path('cart/<int:pk>/', views.CartDetailView.as_view(), name='cart-detail'),
    path('whishlist/add/', views.AddToWishListView.as_view(), name='whishlist-add'),
    path('review/add/', views.AddReviewToProduct.as_view(), name='add-review'),
    path('review/update/', views.UpdateReview.as_view(), name='update-review'),
    path('review/delete/<int:pk>', views.DeleteReview.as_view(), name='add-review'),
    path('search/', views.SearchProductView.as_view(), name='search-product'),
    path('create_checkout_session/', views.create_checkout_session, name='create_checkout_session'),
    # path("create_checkout_session/", views.create_checkout_session, name="create_checkout_session"),
    path("webhook", views.my_webhook_view, name="webhook"),

    # Newly Added

    path("get_orders", views.get_orders, name="get_orders"),
    path("create_user/", views.create_user, name="create_user"),
    path("existing_user/<str:email>", views.existing_user, name="existing_user"),
    path("add_address/", views.add_address, name="add_address"),
    path("get_address", views.get_address, name="get_address"),
    path("my_wishlists", views.my_wishlists, name="my_wishlists"),
    path("product_in_wishlist", views.product_in_wishlist, name="product_in_wishlist"),
    path("get_cart/<str:cart_code>", views.get_cart, name="get_cart"),
    path("get_cart_stat", views.get_cart_stat, name="get_cart_stat"),
    path("product_in_cart", views.product_in_cart, name="product_in_cart")

]