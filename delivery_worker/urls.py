from django.urls import path
from . import views

urlpatterns = [

    # Delivery Assignments
    path('delivery-assignments/', views.DeliveryAssignmentListCreateView.as_view(), name='delivery-assignment-list-create'),
    path('delivery-assignments/<int:pk>/', views.DeliveryAssignmentDetailView.as_view(), name='delivery-assignment-detail'),
]