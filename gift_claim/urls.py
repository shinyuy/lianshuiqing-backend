from django.urls import path
from . import views

urlpatterns = [
    path('gift-claims/', views.GiftClaimListCreateView.as_view(), name='gift-claim-list-create'),
    path('gift-claims/<int:pk>/', views.GiftClaimDetailView.as_view(), name='gift-claim-detail'),
]
