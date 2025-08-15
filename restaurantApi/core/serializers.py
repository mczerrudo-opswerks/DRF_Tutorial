from rest_framework import serializers
from .models import Restaurant, MenuItem, Order, OrderItem, Review

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ("id","restaurant","name","price","is_available","created_at")
        read_only_fields = ("created_at",)