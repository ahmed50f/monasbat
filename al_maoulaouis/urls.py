from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/hall/', include('hall.urls')),
    path('api/DJ/', include('DJ.urls')),
    path('api/musical_band/', include('musical_band.urls')),
    path('api/lights/', include('lights.urls')),
    path('api/reservation/', include('reservation.urls')),
    path('api/cart/', include('cart.urls')),
]
