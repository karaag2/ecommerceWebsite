from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view 
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics, status, mixins
from django.db.models import Q
from rest_framework.response import Response
from .models import CustomUser, Product, ProductCategory, Cart, CartItem, Review, Wishlist
from .serializers import (
    ProductListSerializer,
    ProductDetailedSerializer, 
    ProductCategoryListSerializer, 
    ProductCategoryDetailedSerializer, 
    CartItemSerializer, 
    CartSerializer,
    ReviewSerializer,
    WishlistSerializer
)
# Create your views here.

class ProductList(generics.ListAPIView):
    queryset = Product.objects.filter(featured=True)
    serializer_class = ProductListSerializer

class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailedSerializer
    lookup_field = 'slug'

class CategoryList(generics.ListAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategoryListSerializer

class CategoryDetailed(generics.RetrieveAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategoryDetailedSerializer
    lookup_field = 'slug'


class AddToCartView(generics.CreateAPIView):
    """
    API view for adding items to cart.
    Handles both creating new cart items and updating existing ones.
    Returns the complete cart with all its items.
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        cart_code = request.data.get('cart_code')
        product_id = request.data.get('product_id')
        
        # Validate required fields
        if not cart_code or not product_id:
            return Response(
                {'error': 'Both cart_code and product_id are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Get or create cart
            cart, _ = Cart.objects.get_or_create(cart_code=cart_code)
            
            # Get product or return 404
            product = get_object_or_404(Product, id=product_id)

            # Get or create cart item with default quantity of 1
            cart_item, created = CartItem.objects.get_or_create(
                product=product,
                cart=cart,
                defaults={'quantity': 1}  # One is the default quantity
            )

            # If the item already exists, increment quantity by 1
            if not created:
                cart_item.quantity += 1
                cart_item.save()

            # Serialize the complete cart for response
            cart_serializer = CartSerializer(cart)
            return Response(
                cart_serializer.data,
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
            )

        except Product.DoesNotExist:
            return Response(
                {'error': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
class DeleteCartItemView(generics.RetrieveAPIView):
    """
    API view for retrieving cart item details
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [AllowAny]


class UpdateCartItemView(generics.UpdateAPIView):
    """
    API view for updating cart item quantity
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [AllowAny]
    def update(self, request, *args,**kwargs):
        quantity = request.data.get('quantity')
        cart_item = self.get_object()
        if quantity is not None:
            cart_item.quantity += quantity
            cart_item.save()
            return Response(self.get_serializer(cart_item).data)
class UpdateCartItemAlternativeView(generics.UpdateAPIView):
    """
    Alternative API view for updating cart item quantity using body params
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [AllowAny]

    def update(self, request, *args, **kwargs):
        cart_item = self.get_object()
        quantity = request.data.get('quantity')
        if quantity is not None:
            cart_item.quantity += int(quantity)
            cart_item.save()
            return Response(self.get_serializer(cart_item).data)
        quantity = request.data.get('quantity')
        print(quantity, cart_item_id)
        try:
            cart_item = CartItem.objects.get(id=cart_item_id)
            cart_item.quantity += int(quantity)
            cart_item.save()

            cart_serializer = CartItemSerializer(cart_item)
            return Response(cart_serializer.data,)

        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Cart item not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError:
            return Response(
                {'error': 'Invalid quantity'},
                status=status.HTTP_400_BAD_REQUEST
            )
    lookup_field = 'pk'
class CartDetailView(generics.DestroyAPIView):
    """
    API view for deleting cartitems
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'

class AddReviewToProduct(generics.CreateAPIView):
    """
    API view for adding a review to a product
    """
    queryset = Product.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]
class UpdateReview(generics.UpdateAPIView):
    """
    API view for updating a review
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    def update(self, request):
        user_email = request.user.email
        product = request.data.get('product')
        rate = request.data.get('rating')
        review_data = request.data.get('comment')

        try:
            review = Review.objects.get(user__email=user_email, product__id=product)
            review.rating = rate
            review.comment = review_data
            review.save()
            return Response(self.get_serializer(review).data)
        except Review.DoesNotExist:
            return Response(
                {'error': 'Review not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
class DeleteReview(generics.DestroyAPIView):
    """
    API view for deleting a review
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'


class AddToWishListView(generics.GenericAPIView):
    """
    API view for adding a product to the wishlist
    """
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
         product_id = request.data.get('product')
         user_email = request.user.email

         user = CustomUser.objects.get(email=user_email)
         product = get_object_or_404(Product, id=product_id)

         wishlist = Wishlist.objects.filter(user=user, product=product)

         if wishlist.exists():
             wishlist.delete()
             return Response({'error': 'Product already in wishlist'}, status=status.HTTP_400_BAD_REQUEST)

         new_wishlist = Wishlist.objects.create(user=user, product=product)
         return Response(self.get_serializer(new_wishlist).data, status=status.HTTP_201_CREATED)

class RemoveFromWishListView(generics.DestroyAPIView):
    """
    API view for removing a product from the wishlist
    """
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'
class SearchProductView(generics.GenericAPIView):
    """
        API view for search a product by providing a search input
    """
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query', '').strip()
        if not query:
            return Response({"error":"No query provided"}, 
                            status=status.HTTP_400_BAD_REQUEST
                            )
        products = Product.objects.filter(Q(name__icontains=query)|
                                          Q(description__icontains=query)|
                                          Q(category__name__icontains=query))
        print(products)
        return Response(self.get_serializer(products, many=True).data, status=status.HTTP_200_OK)
