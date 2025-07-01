from django.urls import path
from . import views

urlpatterns = [

    # Waiter Feedback
    path('waiter-feedback/', views.WaiterFeedbackListCreateView.as_view(), name='waiter-feedback-list-create'),
    path('waiter-feedback/<int:pk>/', views.WaiterFeedbackDetailView.as_view(), name='waiter-feedback-detail'),
]