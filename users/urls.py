from django.urls import path
from users import views

urlpatterns = [
    # ---------------------------
    # Health Check
    # ---------------------------
    path("ping", views.ping, name="ping"),


    # ---------------------------
    # Authentication
    # ---------------------------
    path("login", views.login_view, name="login_user"),
    path("logout", views.logout_view, name="logout_user"),
    path("refresh", views.refresh_view, name="refresh_token"),
    path("csrf/", views.get_csrf, name="csrf"),


    # ---------------------------
    # User Management
    # ---------------------------
    path("register", views.register_user, name="register_user"),
    path("user", views.user_view, name="current_user"),
    path("users/me", views.user_view, name="current_user_profile"),
    path("current-user/", views.current_user, name="current-user"),
]