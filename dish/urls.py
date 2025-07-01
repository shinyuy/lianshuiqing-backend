from django.urls import path
from . import views

urlpatterns = [

    # Delivery Assignments
    path('dish/', views.DishListCreateView.as_view(), name='dish'),
    path('dish/<int:pk>/', views.DishRetrieveUpdateDestroyView.as_view(), name='dish-detail'),
]