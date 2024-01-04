from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, APIView
from rest_framework import authentication, permissions, throttling
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import generics
from django.core.paginator import Paginator, EmptyPage
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination


from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer, OrderItemSerializer
from .filters import MenuItemFilter

# Create your views here.

class CategoryView(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MenuItemView(viewsets.ReadOnlyModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MenuItemFilter
    search_fields = ["title"]
    ordering_fields = ["price", "category"]
    pagination_class = PageNumberPagination

    
  
class CartListView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    
    def get_queryset(self):
        c_user = self.request.user
        if c_user.is_staff:
            return Cart.objects.all()
        return Cart.objects.filter(user=c_user)
  
class OrderView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        c_user = self.request.user
        if c_user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=c_user)
    
  
class OrderItemView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderItemSerializer
    
    def get_queryset(self):
        c_user = self.request.user
        if c_user.is_staff:
            return OrderItem.objects.all()
        return OrderItem.objects.filter(user=c_user)
    