from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import custom_user,product, product_category
# Register your models here.
class custom_user_admin (UserAdmin):
    list_display = ['username', 'email', 'first_name']
admin.site.register(custom_user,UserAdmin)

class product_admin(admin.ModelAdmin):
    list_display = ['name', 'price', 'featured']
admin.site.register( product,product_admin)

class category_admin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'image']
admin.site.register(product_category,category_admin)
