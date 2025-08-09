from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HallViewSet, PopularHallsViewSet, Extra_PackagesViewSet, Basic_PackagesViewSet

router = DefaultRouter()
router.register(r'Hall', HallViewSet, basename='hall')
router.register(r'Extra_Bakage', Extra_PackagesViewSet, basename='extra_bakges')
router.register(r'Basic_Backage', Basic_PackagesViewSet, basename='basic_bakges')
router.register(r'PopularHallsViewSet',PopularHallsViewSet , basename='popularHall')

urlpatterns = router.urls
