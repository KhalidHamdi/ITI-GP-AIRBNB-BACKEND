import django_filters
from .models import Property

class PropertyFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')
    keyword = django_filters.CharFilter(field_name="name", lookup_expr='icontains')
    guests = django_filters.NumberFilter(field_name='guests', lookup_expr='gte')
    minprice = django_filters.NumberFilter(field_name="price_per_night", lookup_expr='gte')
    maxprice = django_filters.NumberFilter(field_name="price_per_night", lookup_expr='lte')
    country =  django_filters.CharFilter(field_name="country", lookup_expr='iexact')

    class Meta:
        model = Property
        fields = ('category', 'price_per_night', 'country', 'guests', 'name', 'keyword', 'minprice', 'maxprice')