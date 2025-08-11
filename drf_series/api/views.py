from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from api.models import Product, Order, OrderItem
from api.serializers import ProductSerializer, OrderSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def product_list(request):
    """
    List all products
    """
    products = Product.objects.all()
    # use many=True to serialize multiple objects
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data,200)  # HTTP 200 OK

# Create your views here.
@api_view(['GET'])
def product_detail(request, pk):
    """
    Retrieve a product by its ID
    """
    product = get_object_or_404(Product, pk=pk)
    # Serialize a single object
    serializer = ProductSerializer(product)
    return Response(serializer.data, 200)  # HTTP 200 OK

@api_view(['GET'])
def order_list(request):
    """
    List all orders
    """
    orders = Order.objects.all()
    # use many=True to serialize multiple objects
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data,200)  # HTTP 200 OK