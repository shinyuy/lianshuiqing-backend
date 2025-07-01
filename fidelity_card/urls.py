from django.urls import path
from . import views

urlpatterns = [
    # Fidelity Cards
    path('fidelity-cards/', views.FidelityCardListCreateView.as_view(), name='fidelity-card-list-create'),
    path('fidelity-cards/<int:pk>/', views.FidelityCardDetailView.as_view(), name='fidelity-card-detail'),
]