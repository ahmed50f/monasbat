from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LightViewSet

router = DefaultRouter()
router.register(r'lights', LightViewSet, basename='lights')

urlpatterns = router.urls