import logging
from django.shortcuts import render
from rest_framework import filters, generics, viewsets
from core.models import Restaurant, MenuItem, Order, OrderItem, Review
from core.serializers import (
    MenuItemSerializer,
    RestaurantSerializer,
    OrderCreateSerializer,
    OrderSerializer,
    ReviewSerializer
)
from rest_framework import permissions

logger = logging.getLogger('restaurantAPI')


# Custom Permissions
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: 
            return True
        return getattr(obj, "user_id", None) == request.user.id

# Create your views here.

class MenuItemListCreateAPIView(generics.ListCreateAPIView):
    """
    List all Menu Items
    """
    queryset = MenuItem.objects.order_by('pk').select_related("restaurant")
    serializer_class = MenuItemSerializer

class MenuItemRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a Menu Item by its ID
    """
    queryset = MenuItem.objects.order_by('pk')
    serializer_class = MenuItemSerializer
    permission_classes =  [permissions.AllowAny]
    lookup_url_kwarg = 'menu_id' # Use this if you don't use pk in the URL

    def get_permissions(self):
        if self.request.method in ['PUT','PATCH', 'DELETE']:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["name"]
    ordering_fields = ["name"]

    def perform_create(self, serializer):
        restaurant = serializer.save(owner=self.request.user)
        logger.info(f"Restaurant created: {restaurant.name} by {self.request.user}")

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = OrderSerializer
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).select_related("restaurant", "user").prefetch_related("items__menu_item")   
    
    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)
        logger.info(f"Restaurant created: {order.order_id} by {self.request.user}")

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update": 
            return OrderCreateSerializer
        return super().get_serializer_class()

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    def get_queryset(self):
        return Review.objects.select_related("restaurant","user")
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

