import django_filters
from api.models import Product, Order
from rest_framework import filters


class InStockFilterBackend(filters.BaseFilterBackend):
    """
    Custom filter backend to filter products that are in stock.
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['exact', 'icontains'],
            'price': ['exact', 'lt', 'gt', 'range']
        }


class OrderFilter(django_filters.FilterSet):
    # Purpose of this is to get the Date from the DateTime Field
    created_at = django_filters.DateFilter(field_name='created_at__date')
    class Meta:
        model = Order
        fields = {
            'status': ['exact'],
            'created_at': ['lt', 'gt', 'exact']
        }