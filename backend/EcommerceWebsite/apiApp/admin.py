from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Cart, CustomUser,Product, ProductCategory, CartItem
# Register your models here.
class custom_user_admin (UserAdmin):
    list_display = ['username', 'email', 'first_name']
admin.site.register(CustomUser,UserAdmin)

class product_admin(admin.ModelAdmin):
    list_display = ['name', 'price', 'featured']
admin.site.register( Product,product_admin)

class category_admin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'image']
admin.site.register(ProductCategory,category_admin)

class cart_admin(admin.ModelAdmin):
    list_display = ['cart_code', 'created_at', 'get_cart_items']
    
    def get_cart_items(self, obj):
        return ", ".join([f"{item.product.name} (x{item.quantity})" for item in obj.cartitems.all()])

    get_cart_items.short_description = "Cart Items"
admin.site.register(Cart, cart_admin)
class cart_items_admin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'get_sub_total']

    def get_sub_total(self, obj):
        return obj.quantity * obj.product.price

    get_sub_total.short_description = "Sub Total"
admin.site.register(CartItem, cart_items_admin)
