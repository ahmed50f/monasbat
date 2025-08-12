from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LightViewSet, UserLightViewSet

router = DefaultRouter()
router.register(r'lights', LightViewSet, basename='lights')
router.register(r'user_light', UserLightViewSet, basename='user_light')
urlpatterns = router.urls