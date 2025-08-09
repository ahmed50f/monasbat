from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Musical_BandViewSet, TopBandViewSet

router = DefaultRouter()
router.register(r'musical_band', Musical_BandViewSet, basename= 'musical_band')
router.register(r'TopBand', TopBandViewSet, basename= 'topband')

urlpatterns = router.urls