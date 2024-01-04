from django_filters.rest_framework import FilterSet
from rest_framework import filters
import django_filters
from .models import MenuItem


class MenuItemFilter(FilterSet):
    class Meta:
        model = MenuItem
        fields = {
            'id': ['exact'],
            'price': ['gt', 'lt'],
            # "featured": ['isTrue', 'isFalse']
            
        }
        
