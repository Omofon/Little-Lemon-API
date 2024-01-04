from rest_framework_nested import routers
from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter

router = routers.DefaultRouter()
router.register(r"menu-items", views.MenuItemView, basename="menu-items"),
router.register(r"category", views.CategoryView, basename="category"),
router.register(r"cart", views.CartListView, basename="cart-list"),
router.register(r"order", views.OrderView, basename="order"),
router.register(r"order-items", views.OrderItemView, basename="order-items"),

order_router = routers.NestedSimpleRouter(router, "order", lookup="order")
order_router.register("order-items", views.OrderItemView, basename="order-items")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(order_router.urls)),
]