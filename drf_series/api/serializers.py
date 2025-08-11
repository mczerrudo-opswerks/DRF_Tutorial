from rest_framework import serializers
from .models import Product, Order, OrderItem

# Serializers handles converting data to JSON and validating input data
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'price',
            'stock',
        )

    # validate_[field_name] methods are used to validate specific fields
    def validate_price(self, value):
        """
        Validate price field
        """
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than 0."
            )
        return value