from django.shortcuts import render
from rest_framework.decorators import api_view 
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from .models import product, product_category
from .serializers import product_list_serializer,product_detailed_serializer, product_category_list_serializer, product_category_detailed_serializer
# Create your views here.

class product_list(generics.ListAPIView):
    queryset = product.objects.filter(featured=True)
    serializer_class = product_list_serializer

class product_detail(generics.RetrieveAPIView):
    queryset = product.objects.all()
    serializer_class = product_detailed_serializer
    lookup_field = 'slug'

class category_list(generics.ListAPIView):
    queryset = product_category.objects.all()
    serializer_class = product_category_list_serializer

class category_detailed(generics.RetrieveAPIView):
    queryset = product_category.objects.all()
    serializer_class = product_category_detailed_serializer
    lookup_field = 'slug'