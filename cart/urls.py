# urls.py
from rest_framework.routers import DefaultRouter
from .views import UserDJViewSet, UserMusicalBandViewSet, UserLightViewSet, CartItemViewSet

router = DefaultRouter()
router.register(r'user-djs', UserDJViewSet, basename='userdj')
router.register(r'user-bands', UserMusicalBandViewSet, basename='userband')
router.register(r'user-lights', UserLightViewSet, basename='userlight')
router.register(r'cart-items', CartItemViewSet, basename='cartitem')

urlpatterns = router.urls
