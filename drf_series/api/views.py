from django.db.models import Max
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from api.models import Product, Order, OrderItem
from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics

# Class based views for product list
class ProductListAPIView(generics.ListAPIView):
    """
    List all products
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Class based views for product detail
class ProductDetailAPIView(generics.RetrieveAPIView):
    """
    Retrieve a product by its ID
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id' # Use this if you don't use pk in the URL


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

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        'products': products,
        'count': len(products),
        # Learn more about Django ORM aggregation functions
        'max_price': products.aggregate(max_price=Max('price'))['max_price'] or 0
    })
    return Response(serializer.data, 200)  # HTTP 200 OK 