import django_filters

from .models import Property ;

class PropertyFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')
    keyword = django_filters.filters.CharFilter(field_name="name",  lookup_expr='icontains')
    minprice =  django_filters.NumberFilter(field_name="price_per_night" or 0, lookup_expr='gte')
    maxprice =  django_filters.NumberFilter(field_name="price_per_night" or 3000 ,  lookup_expr='lte')

    class Meta:
        model = Property
        # fields = ['price_per_night', 'country' , 'guests']
        fields = ( 'category','price_per_night', 'country' , 'guests' ,  'name' , 'keyword' , 'minprice' , 'maxprice') 