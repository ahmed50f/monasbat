from django.urls import path
from . import views
from .views import NotificationViewSet

notification_list = NotificationViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

notification_detail = NotificationViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

mark_as_read = NotificationViewSet.as_view({
    'post': 'mark_as_read'
})


urlpatterns = [
    # Authentication & Registration
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),

    # OTP & Verification
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("verify-forgot-password-otp/", views.verify_forgot_password_otp, name="verify_forgot_password_otp"),

    # Password Management
    path("reset-password/", views.reset_password, name="reset_password"),
    path("change-password/", views.change_password, name="change_password"),

    # Profile
    path("profile/", views.UserProfileView.as_view(), name="user_profile"),

    # Notifications
    path('notifications/', notification_list, name='notification-list'),
    path('notifications/<int:pk>/', notification_detail, name='notification-detail'),
    path('notifications/<int:pk>/mark_as_read/', mark_as_read, name='notification-mark-as-read'),
]

    
