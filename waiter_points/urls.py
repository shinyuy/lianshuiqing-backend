from django.urls import path
from . import views

urlpatterns = [
    # Waiter Points
    path('waiter-points/', views.WaiterPointsListCreateView.as_view(), name='waiter-points-list-create'),
    path('waiter-points/<int:pk>/', views.WaiterPointsDetailView.as_view(), name='waiter-points-detail'),
]