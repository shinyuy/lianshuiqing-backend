from django.urls import path
from . import views

urlpatterns = [
    # Raffle Entries
    path('raffle-entries/', views.RaffleEntryListCreateView.as_view(), name='raffle-entry-list-create'),
    path('raffle-entries/<int:pk>/', views.RaffleEntryDetailView.as_view(), name='raffle-entry-detail'),
]
