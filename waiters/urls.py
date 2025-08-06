from django.urls import path
from .views import (
    InviteWaiterApiView,
    ListWaitersApiView,
    DeleteWaiterApiView,
    GetSingleWaiterApiView,
    ChangePasswordApiView
)

urlpatterns = [
    path('waiters/invite/', InviteWaiterApiView.as_view(), name='invite-waiter'),
    path('waiters/', ListWaitersApiView.as_view(), name='list-waiters'),
    path('waiters/<int:waiter_id>/', GetSingleWaiterApiView.as_view(), name='get-single-waiter'),
    path('waiters/<int:waiter_id>/delete/', DeleteWaiterApiView.as_view(), name='delete-waiter'),
    path('change-password/', ChangePasswordApiView.as_view(), name='change-password'),
]
  