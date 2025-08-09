from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DJViewSet, TopDJViewSet

router = DefaultRouter()
router.register(r'dj', DJViewSet, basename='DJ')
router.register(r'TopDJ', TopDJViewSet, basename='topdj')
urlpatterns = router.urls
   