from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DJViewSet, TopDJViewSet, UserDJViewSet

router = DefaultRouter()
router.register(r'dj', DJViewSet, basename='DJ')
router.register(r'top_dj', TopDJViewSet, basename='topdj')
router.register(r'user_dj', UserDJViewSet, basename='userdj')
urlpatterns = router.urls
   