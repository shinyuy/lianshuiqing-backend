from django.urls import path
from . import views

urlpatterns = [
    # Payments
    # path('payments/', views.PaymentListCreateView.as_view(), name='payment-list-create'),
    # path('payments/<int:pk>/', views.PaymentDetailView.as_view(), name='payment-detail'),
    path("momo/pay/", views.MomoCartPaymentApiView.as_view()),
    path("orange/pay/", views.orange_money_payment, name="orange-payment"),
]
