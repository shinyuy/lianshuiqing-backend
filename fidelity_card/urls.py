from django.urls import path
from . import views

urlpatterns = [
    # Fidelity Cards
    path('admin/fidelity-cards', views.FidelityCardApiView.as_view(), name='fidelity-cards'),
    path('admin/fidelity-cards/<int:id>', views.DeleteFidelityCardApiView.as_view(), name='fidelity-card-detail'),
]