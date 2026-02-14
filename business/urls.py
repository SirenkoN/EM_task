"""URL-маршруты для бизнес-логики."""

from django.urls import path
from .views import ProductListView, OrderListView, UserListView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('users/', UserListView.as_view(), name='user-list'),
]
