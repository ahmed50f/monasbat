from django.urls import path
from . import views

urlpatterns = [
    path('payment/stripe_initialize/', views.stripe_initialize, name='stripe_initialize'),
    path('payment/stripe_webhook/', views.stripe_webhook, name='stripe_webhook'),
]