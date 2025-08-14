
from django.db import transaction
from rest_framework import serializers
from .models import Product, Order, OrderItem, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'is_staff',
        )




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

class OrderCreateSerializer(serializers.ModelSerializer):
    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderItem
            fields = (
                'product',
                'quantity'
            )

    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemCreateSerializer(many=True, default = None)

    def update(self,instance, validated_data):
        orderitem_data = validated_data.pop('items')
        
        with transaction.atomic(): # something fails inside it goes back to the db goes back to its initial state
            instance = super().update(instance,validated_data)

            if orderitem_data is not None:
                # Clear existing items (optional)
                instance.items.all().delete()

                # Re add the items with the updated data
                for item in orderitem_data:
                    OrderItem.objects.create(order=instance,**item)


        return instance

    # Override the Create function of a serializer
    def create(self, validated_data):
        orderitem_data = validated_data.pop('items')

        with transaction.atomic():
            order = Order.objects.create(**validated_data)

            for item in orderitem_data:
                OrderItem.objects.create(order=order,**item)

        return order
    class Meta:
        model = Order
        fields = (
            'order_id',
            'user',
            'status',
            'items',
        )
        extra_kwargs = {
            'user': {'read_only': True}
        }

class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True)  # read_only means this field is not required for input, but will be included in output
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