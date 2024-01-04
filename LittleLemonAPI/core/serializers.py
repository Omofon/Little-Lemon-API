from django.contrib.auth.models import User
from rest_framework import serializers

from .models import MenuItem, Category, Cart, Order, OrderItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title"]


class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = MenuItem
        fields = ["id", "title", "category", "price", "featured"]

class SimpleMenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['title', 'price']
        
class CartSerializer(serializers.ModelSerializer):
    menuitem = SimpleMenuItemSerializer(many=False)
    user = UserSerializer()
    total_price = serializers.SerializerMethodField(method_name="total", read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'quantity', 'total_price']
        extra_kwargs = {
            'quantity': {'min_value': 1},
        }
        
    def total(self, cartitem: Cart):
        return cartitem.menuitem.price * cartitem.quantity


class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = SimpleMenuItemSerializer(many=False)
    sub_price = serializers.SerializerMethodField(method_name="item_price", read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'menuitem', 'quantity', 'sub_price']
        extra_kwargs = {
            'quantity': {'min_value': 1},
        }

    def item_price(self, orderitem: OrderItem):
        return orderitem.quantity * orderitem.menuitem.price

class OrderSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    status = serializers.BooleanField(read_only=True)
    date = serializers.DateField(read_only=True)
    delivery_crew = serializers.CharField(read_only=True)
    grand_total = serializers.SerializerMethodField(method_name='main_total')
    items = OrderItemSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    
    class Meta:
        model = Order
        fields = ['id', 'user','items', 'delivery_crew','status', 'date','grand_total']
        
    def main_total(self, order: Order):
        items = order.items.all()
        total = sum([item.quantity * item.menuitem.price for item in items])
        return total