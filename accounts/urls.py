from django.urls import path
from . import views

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
]
