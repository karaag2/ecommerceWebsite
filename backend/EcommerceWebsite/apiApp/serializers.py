from rest_framework import serializers
from .models import custom_user, product, product_category

class product_list_serializer(serializers.ModelSerializer):
    class Meta:
        model = product
        fields=['id','name','slug','image','price']
        
class product_detailed_serializer(serializers.ModelSerializer):
    class Meta:
        model = product
        fields=['id','name','description','slug','image','price']

class product_category_list_serializer(serializers.ModelSerializer):
    products = product_list_serializer(many=True, read_only=True)
    class Meta:
        model = product_category
        fields=['id','name','slug','image']

class product_category_detailed_serializer(serializers.ModelSerializer):
    products = product_list_serializer(many=True, read_only=True)
    class Meta:
        model = product_category
        fields=['id','name','slug','image', 'products']