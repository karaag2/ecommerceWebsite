from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import  CustomUser, Product, ProductCategory, Cart, CartItem, Review, Wishlist, Order, OrderItem, CustomerAddress

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields=['id','name','slug','image','price']
        
class ProductDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields=['id','name','description','slug','image','price']

class ProductCategoryListSerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True, read_only=True)
    class Meta:
        model = ProductCategory
        fields=['id','name','slug','image']

class ProductCategoryDetailedSerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True, read_only=True)
    class Meta:
        model = ProductCategory
        fields=['id','name','slug','image', 'products']
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    sub_total = serializers.SerializerMethodField()
    cart_code = serializers.CharField(write_only=True, required=False)
    product_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'cart', 'quantity', 'sub_total', 'cart_code', 'product_id']
        read_only_fields = ['id', 'product', 'cart']

    def get_sub_total(self, cart_item):
        return cart_item.product.price * cart_item.quantity

class CartSerializer(serializers.ModelSerializer):
    cartitems = CartItemSerializer(read_only=True, many=True)
    cart_total = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'cart_code', 'cartitems', 'cart_total']

    def get_cart_total(self, cart):
        items = cart.cartitems.all()
        total = sum(item.product.price * item.quantity for item in items)
        return total
        
class CartStateSerializer(serializers.ModelSerializer):
    total_quantity = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'created_at', 'updated_at', 'total_quantity']

    def get_total_quantity(self, cart):
        items = cart.cart_items.all()
        total = sum(item.quantity for item in items)
        return total

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile_picture_url']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created', 'updated', 'product']
class WishlistSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductListSerializer(read_only=True)
    class Meta:
        model = Wishlist 
        fields = ["id", "user", "product", "created"]



# NEW ADDED 

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ["id", "quantity", "product"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(read_only=True, many=True)
    class Meta:
        model = Order 
        fields = ["id", "stripe_checkout_id", "amount", "items", "status", "created_at"]



class CustomerAddressSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    class Meta:
        model = CustomerAddress
        fields = "__all__"


class SimpleCartSerializer(serializers.ModelSerializer):
    num_of_items = serializers.SerializerMethodField()
    class Meta:
        model = Cart 
        fields = ["id", "cart_code", "num_of_items"]

    def get_num_of_items(self, cart):
        num_of_items = sum([item.quantity for item in cart.cartitems.all()])
        return num_of_items