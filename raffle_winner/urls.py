from django.urls import path
from . import views

urlpatterns = [
    path('raffle-winners/', views.RaffleWinnerListCreateView.as_view(), name='raffle-winner-list-create'),
    path('raffle-winners/<int:pk>/', views.RaffleWinnerDetailView.as_view(), name='raffle-winner-detail'),
]
