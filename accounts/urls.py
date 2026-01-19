from django.urls import path
from .views import RegisterView, LoginView, ProfileView, LogoutView, CookieTokenRefreshView

urlpatterns = [
    path("register", RegisterView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path("me", ProfileView.as_view(), name="me"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("token/refresh", CookieTokenRefreshView.as_view(), name="cookie_token_refresh"),
]
