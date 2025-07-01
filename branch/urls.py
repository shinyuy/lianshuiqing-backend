from django.urls import path
from . import views

urlpatterns = [
    # Branches
    path('branches/', views.BranchListCreateView.as_view(), name='branch-list-create'),
    path('branches/<int:pk>/', views.BranchDetailView.as_view(), name='branch-detail'),
]