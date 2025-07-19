from django.urls import path
from . import views

urlpatterns = [

    # Delivery Assignments
    path('admin/dishes', views.AddDishApiView.as_view(), name='add_dish'),
    path('dishes/get', views.GetDishApiView.as_view(), name='get_dish'),
    path('admin/dishes/<int:id>', views.EditDeleteDishApiView.as_view(), name='dish-detail'),
    path('admin/file/upload', views.FileApiView.as_view()),
]