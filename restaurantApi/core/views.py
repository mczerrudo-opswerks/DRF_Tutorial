from django.shortcuts import render
from rest_framework import filters, generics, viewsets

# Create your views here.

class MenuItemListCreateAPIView(generics.ListCreateAPIView):
    """
    List all Menu Items
    """
    queryset = Product.objects.order_by('pk')
    serializer_class = ProductSerializer
