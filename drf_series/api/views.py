from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import InStockFilterBackend, OrderFilter, ProductFilter
from api.models import Order, OrderItem, Product
from api.serializers import (OrderSerializer, ProductInfoSerializer,
                             ProductSerializer)


# Class based views for product list and create
class ProductListCreateAPIView(generics.ListCreateAPIView):
    """
    List all products and create a new product
    """
    queryset = Product.objects.order_by('pk')
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter,
        filters.OrderingFilter,
        #InStockFilterBackend
    ]
    search_fields = ['name', 'description']  # Optional: Add search functionality
    ordering_fields = ['name', 'price', 'stock']  # Optional: Add ordering functionality

    # Pagination Settings
    pagination_class = PageNumberPagination
    pagination_class.page_size = 2 # Optional: Set page size for pagination
    pagination_class.page_query_param = 'pagenum'  # Optional: Set query param for pagination
    pagination_class.page_size_query_param = 'page_size'  # Optional: Allow client to set page size
    pagination_class.max_page_size = 6  # Optional: Set max page size

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



class OrderViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing order instances.
    """
    queryset = Order.objects.prefetch_related('items__product').all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None  # Disable pagination
    filterset_class = OrderFilter
    filter_backends = [
        DjangoFilterBackend, 
    ]

    # url_path so that the router understand this route
    @action(
            detail=False, 
            methods= ['get'], 
            url_path='user-orders',
            #permission_classes = [IsAuthenticated]
        )
    def user_orders(self,request):
        orders = self.get_queryset().filter(user=request.user)
        # many=True because we're gonna pass multiple orders
        serializer = self.get_serializer(orders,many=True)
        return Response(serializer.data)

# class OrderListAPIView(generics.ListAPIView):
#     """
#     List all orders
#     """
#     queryset = Order.objects.prefetch_related('items__product').all()
#     serializer_class = OrderSerializer 

# class UserOrderListAPIView(generics.ListAPIView):
#     """
#     List all orders
#     """
#     queryset = Order.objects.prefetch_related('items__product').all()
#     serializer_class = OrderSerializer 
#     permission_classes = [IsAuthenticated]  # Add your permission classes here

#     def get_queryset(self):
#         # This is equal to Order.objects.prefetch_related('items__product').filter(user=self.request.user)
#         qs = super().get_queryset()
#         return qs.filter(user=self.request.user)

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