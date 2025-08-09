from django.urls import path
from .views import ReservationApiView, ReservationDetailApiView, CancelReservationApiView

urlpatterns = [
    path('reservations/', ReservationApiView.as_view(), name='reservation-list-create'),
    path('client/reservations/', ReservationApiView.as_view(), name='client-reservation-list-create'),
    path('reservations/<int:pk>/', ReservationDetailApiView.as_view(), name='reservation-detail'),
    path('reservations/<int:pk>/cancel/', CancelReservationApiView.as_view(), name='reservation-cancel'),
]
