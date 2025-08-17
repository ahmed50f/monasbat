from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReservationViewSet, book_hall

router = DefaultRouter()
router.register(r'reservation', ReservationViewSet, basename='reservation')


urlpatterns = [
    path('', include(router.urls)),
    path('book/<str:name>/<str:date>/', book_hall, name='book_hall'),
]
