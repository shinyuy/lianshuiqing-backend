from django.urls import path
from .views import OrderApiView, OrderDetailApiView, CancelOrderApiView

urlpatterns = [
    path('orders/', OrderApiView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailApiView.as_view(), name='order-detail'),
    path('orders/<int:pk>/cancel/', CancelOrderApiView.as_view(), name='order-cancel'),
]