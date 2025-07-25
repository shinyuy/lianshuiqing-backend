"""
URL configuration for bot_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views  
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
   
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('djoser.urls')),
    path('api/', include('users.urls')),
    path('api/', include('branch.urls')),
    path('api/', include('dish.urls')),
    path('api/', include('fidelity_card.urls')),
    path('api/', include('gift_claim.urls')),
    path('api/', include('order.urls')),
    path('api/', include('payment.urls')),  
    path('api/', include('raffle_entry.urls')),
    path('api/', include('raffle_winner.urls')),
    path('api/', include('waiter_feedback.urls')),
    path('api/', include('waiter_points.urls'))
]

