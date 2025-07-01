from django.urls import path
from . import views

urlpatterns = [
    # Payments
    path('payments/', views.PaymentListCreateView.as_view(), name='payment-list-create'),
    path('payments/<int:pk>/', views.PaymentDetailView.as_view(), name='payment-detail'),
]
