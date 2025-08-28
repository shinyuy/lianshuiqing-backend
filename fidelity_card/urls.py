from django.urls import path
from . import views

urlpatterns = [
    # Fidelity Cards
    path('admin/fidelity-cards', views.FidelityCardApiView.as_view(), name='fidelity-cards'),
    path('admin/fidelity-cards/<int:id>', views.DeleteFidelityCardApiView.as_view(), name='fidelity-card-detail'),

  # Fidelity Subscription
    path('fidelity-cards/subscribe/momo/', views.MomoFidelitySubscriptionApiView.as_view(), name='fidelity-subscribe-momo'),
    path('fidelity-cards/subscribe/om/', views.OmFidelitySubscriptionApiView.as_view(), name='fidelity-subscribe-om'),
    
      path("users/<int:user_id>/subscriptions/", views.UserFidelityCardSubscriptionsView.as_view(), name="user_subscriptions"),
    path("users/<int:user_id>/subscriptions/active/", views.UserActiveFidelityCardSubscriptionView.as_view(), name="user_active_subscription"),

]