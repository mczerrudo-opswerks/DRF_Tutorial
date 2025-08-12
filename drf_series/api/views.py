from django.db.models import Max
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from api.models import Product, Order, OrderItem
from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny,
)
from rest_framework.views import APIView
from api.filters import ProductFilter

# Class based views for product list and create
class ProductListCreateAPIView(generics.ListCreateAPIView):
    """
    List all products and create a new product
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter

    # Customizing permissions in a Generic View
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


# Class based views for product detail
class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a product by its ID
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id' # Use this if you don't use pk in the URL

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ['PUT','PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

# # Create your views here.
# @api_view(['GET'])
# def product_detail(request, pk):
#     """
#     Retrieve a product by its ID
#     """
#     product = get_object_or_404(Product, pk=pk)
#     # Serialize a single object
#     serializer = ProductSerializer(product)
#     return Response(serializer.data, 200)  # HTTP 200 OK


class OrderListAPIView(generics.ListAPIView):
    """
    List all orders
    """
    queryset = Order.objects.prefetch_related('items__product').all()
    serializer_class = OrderSerializer 

# @api_view(['GET'])
# def order_list(request):
#     """
#     List all orders
#     """
#     # prefetch_related is used to optimize database queries
#     # It reduces the number of queries by fetching related objects in a single query
#     orders = Order.objects.prefetch_related('items__product').all()
#     # use many=True to serialize multiple objects
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data,200)  # HTTP 200 OK

class UserOrderListAPIView(generics.ListAPIView):
    """
    List all orders
    """
    queryset = Order.objects.prefetch_related('items__product').all()
    serializer_class = OrderSerializer 
    permission_classes = [IsAuthenticated]  # Add your permission classes here

    def get_queryset(self):
        # This is equal to Order.objects.prefetch_related('items__product').filter(user=self.request.user)
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

# APIView is good if you have custom logic or need to handle different HTTP methods
class ProductInfoAPIView(APIView):
    """
    Get all products, count of products, and max price
    """
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products': products,
            'count': len(products),
            'max_price': products.aggregate(max_price=Max('price'))['max_price'] or 0
        })
        return Response(serializer.data, 200)  # HTTP 200 OK

# @api_view(['GET'])
# def product_info(request):
#     products = Product.objects.all()
#     serializer = ProductInfoSerializer({
#         'products': products,
#         'count': len(products),
#         # Learn more about Django ORM aggregation functions
#         'max_price': products.aggregate(max_price=Max('price'))['max_price'] or 0
#     })
#     return Response(serializer.data, 200)  # HTTP 200 OK 