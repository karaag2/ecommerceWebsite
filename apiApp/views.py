import stripe
from django.conf import settings

from django.shortcuts import render, get_object_or_404,HttpResponse
from rest_framework.decorators import api_view 
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics, status, mixins
from django.db.models import Q
from rest_framework.response import Response
from .models import CustomUser, Product, ProductCategory, Cart, CartItem, Review, Wishlist,Order, OrderItem
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
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.WEBHOOK_SECRET
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
class CartDetailView(generics.RetrieveAPIView):
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

@api_view(['POST'])
def create_checkout_session(request):
    cart_code = request.data.get("cart_code")
    email = request.data.get("email")
    cart = Cart.objects.get(cart_code=cart_code)
    try:
        checkout_session = stripe.checkout.Session.create(
            customer_email= email,
            payment_method_types=['card'],


            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': item.product.name},
                        'unit_amount': int(item.product.price * 100),  # Amount in cents
                    },
                    'quantity': 5,
                }
                for item in cart.cartitems.all()
            ] + [
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': 'VAT Fee'},
                        'unit_amount': 500,  # $5 in cents
                    },
                    'quantity': 1,
                }
            ],


           
            mode='payment',
            # success_url="http://localhost:3000/success",
            # cancel_url="http://localhost:3000/cancel",

            success_url="http://localhost:3000/profile",
            cancel_url="http://localhost:3000/",
            metadata = {"cart_code": cart_code}
        )
        return Response({'data': checkout_session})
    except Exception as e:
        return Response({'error': str(e)}, status=400)




@csrf_exempt
def my_webhook_view(request):
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, endpoint_secret
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)

  if (
    event['type'] == 'checkout.session.completed'
    or event['type'] == 'checkout.session.async_payment_succeeded'
  ):
    session = event['data']['object']
    cart_code = session.get("metadata", {}).get("cart_code")

    fulfill_checkout(session, cart_code)


  return HttpResponse(status=200)



def fulfill_checkout(session, cart_code):
    
    order = Order.objects.create(stripe_checkout_id=session["id"],
        amount=session["amount_total"],
        currency=session["currency"],
        customer_email=session["customer_email"],
        status="Paid")
    

    print(session)


    cart = Cart.objects.get(cart_code=cart_code)
    cartitems = cart.cartitems.all()

    for item in cartitems:
        orderitem = OrderItem.objects.create(order=order, product=item.product, 
                                             quantity=item.quantity)
    
    cart.delete()


def my_webhook(session,cart_code):
    order = Order.objects.create(stripe_chekout_id=session["id"],
                                amount  =session['ammount_total'],
                                currency=session['currency'],
                                customer_email=session['customer_email'],
                                status='Paid'
                                 )
    
    cart = Cart.objects.get(cart_code=cart_code)
    Cartitems = cart.cartitems.all()

    for item in cartitems:
        orderitem = OrderItem.objects.create(order=order,
                                             product=item.product,
                                             quantity=item.quantity)
    cart.delete

@api_view(["POST"])
def create_user(request):
    username = request.data.get("username")
    email = request.data.get("email")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")
    profile_picture_url = request.data.get("profile_picture_url")

    new_user = User.objects.create(username=username, email=email,
                                       first_name=first_name, last_name=last_name, profile_picture_url=profile_picture_url)
    serializer = UserSerializer(new_user)
    return Response(serializer.data)


@api_view(["GET"])
def existing_user(request, email):
    try:
        User.objects.get(email=email)
        return Response({"exists": True}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"exists": False}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_orders(request):
    email = request.query_params.get("email")
    orders = Order.objects.filter(customer_email=email)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def add_address(request):
    email = request.data.get("email")
    street = request.data.get("street")
    city = request.data.get("city")
    state = request.data.get("state")
    phone = request.data.get("phone")

    if not email:
        return Response({"error": "Email is required"}, status=400)
    
    customer = User.objects.get(email=email)

    address, created = CustomerAddress.objects.get_or_create(
        customer=customer)
    address.email = email 
    address.street = street 
    address.city = city 
    address.state = state
    address.phone = phone 
    address.save()

    serializer = CustomerAddressSerializer(address)
    return Response(serializer.data)


@api_view(["GET"])
def get_address(request):
    email = request.query_params.get("email") 
    address = CustomerAddress.objects.filter(customer__email=email)
    if address.exists():
        address = address.last()
        serializer = CustomerAddressSerializer(address)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"error": "Address not found"}, status=200)


@api_view(["GET"])
def my_wishlists(request):
    email = request.query_params.get("email")
    wishlists = Wishlist.objects.filter(user__email=email)
    serializer = WishlistSerializer(wishlists, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def product_in_wishlist(request):
    email = request.query_params.get("email")
    product_id = request.query_params.get("product_id")

    if Wishlist.objects.filter(product__id=product_id, user__email=email).exists():
        return Response({"product_in_wishlist": True})
    return Response({"product_in_wishlist": False})



@api_view(['GET'])
def get_cart(request, cart_code):
    cart = Cart.objects.filter(cart_code=cart_code).first()
    
    if cart:
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response({"error": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)




@api_view(['GET'])
def get_cart_stat(request):
    cart_code = request.query_params.get("cart_code")
    cart = Cart.objects.filter(cart_code=cart_code).first()

    if cart:
        serializer = SimpleCartSerializer(cart)
        return Response(serializer.data)
    return Response({"error": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def product_in_cart(request):
    cart_code = request.query_params.get("cart_code")
    product_id = request.query_params.get("product_id")
    
    cart = Cart.objects.filter(cart_code=cart_code).first()
    product = Product.objects.get(id=product_id)
    
    product_exists_in_cart = CartItem.objects.filter(cart=cart, product=product).exists()

    return Response({'product_in_cart': product_exists_in_cart})