from rest_framework import serializers
from .models import Product, Order, OrderItem

# Serializers handles converting data to JSON and validating input data
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'description',
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
    
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(
        source='product.price', 
        max_digits=10, 
        decimal_places=2, 
        read_only=True
    )
    class Meta:
        model = OrderItem
        fields = (
            'product_name',
            'product_price',
            'quantity',
            'item_subtotal',
        )

class OrderSerializer(serializers.ModelSerializer):
    # read_only means this field is not required for input, but will be included in output
    # 'items' is a related name for the OrderItem model
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    # obj is the instance of the Order model being serialized
    def get_total_price(self, obj):
        """
        Calculate total price of the order
        """
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)
    class Meta:
        model = Order
        fields = (
            'order_id',
            'created_at',
            'user',
            'status',
            'items',
            'total_price',
        )

# Generic Serializer not tied to a specific model 
class ProductInfoSerializer(serializers.Serializer):
    """
    get all the products, count of products, and max price
    """
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()