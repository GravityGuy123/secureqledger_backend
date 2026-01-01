from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware import csrf
from django.contrib.auth import authenticate
from django.db import IntegrityError

from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import ValidationError

from django.contrib.auth import get_user_model
from .authentication import CookieJWTAuthentication
# from .tasks import send_welcome_email
from .serializers import (
    RegisterSerializer,
    CurrentUserSerializer,
)

User = get_user_model()


# ---------------------------
# PING
# ---------------------------
@api_view(["GET"])
def ping(request):
    return Response({"message": "pong"})


# ---------------------------
# COOKIE HELPERS
# ---------------------------
def get_cookie_settings():
    if settings.DEBUG:
        return {"httponly": True, "secure": False, "samesite": "Lax"}
    return {"httponly": True, "secure": True, "samesite": "None"}


def cookie_settings_for_request(request):
    cs = get_cookie_settings()
    origin = request.headers.get("Origin") or request.META.get("HTTP_ORIGIN")
    trusted = getattr(settings, "CORS_ALLOWED_ORIGINS", []) or []
    normalized_trusted = [u.rstrip("/") for u in trusted]

    if origin and (origin in trusted or origin.rstrip("/") in normalized_trusted):
        return {"httponly": True, "secure": True, "samesite": "None"}
    return cs


# ---------------------------
# REGISTER USER
# ---------------------------
@api_view(["POST"])
def register_user(request):
    try:
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        # # async welcome email
        # send_welcome_email.delay(user.full_name, user.email)

        return Response({
            "id": str(user.id),
            "first_name": user.first_name,
            "last_name": user.last_name,
            "full_name": user.full_name,
            "username": user.username,
            "email": user.email,
            "country": user.country,
            "state": user.state,
        }, status=status.HTTP_201_CREATED)

    except ValidationError as e:
        return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ---------------------------
# LOGIN
# ---------------------------
@api_view(["POST"])
def login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response({"detail": "Email and password required"}, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"detail": "Invalid credentials"}, status=401)

    user = authenticate(request, username=email, password=password)

    if not user:
        return Response({"detail": "Invalid credentials"}, status=401)

    refresh = RefreshToken.for_user(user)

    response = Response({
        "id": str(user.id),
        "first_name": user.first_name,
        "last_name": user.last_name,
        "full_name": user.full_name,
        "username": user.username,
        "email": user.email,
        "country": user.country,
        "state": user.state,
        "is_admin": user.is_admin,
        "is_moderator": user.is_moderator,
    }, status=200)

    set_jwt_cookies(response, str(refresh.access_token), str(refresh), request)
    return response


# ---------------------------
# REFRESH TOKEN
# ---------------------------
@api_view(["POST"])
def refresh_view(request):
    refresh_token = request.COOKIES.get("refresh_token")
    if not refresh_token:
        return Response({"detail": "Refresh token missing"}, status=401)

    try:
        refresh = RefreshToken(refresh_token)
        new_access = str(refresh.access_token)
        new_refresh = str(refresh)

        response = Response({"detail": "Token refreshed"}, status=200)
        set_jwt_cookies(response, new_access, new_refresh, request)
        return response

    except Exception:
        return Response({"detail": "Invalid or expired refresh token. Please login again."}, status=401)


# ---------------------------
# LOGOUT
# ---------------------------
@api_view(["POST"])
def logout_view(request):
    response = Response({"detail": "Logged out successfully"}, status=200)
    cookie_domain = getattr(settings, "COOKIE_DOMAIN", None)

    kwargs = {"path": "/"}
    if cookie_domain:
        kwargs["domain"] = cookie_domain

    response.delete_cookie("access_token", **kwargs)
    response.delete_cookie("refresh_token", **kwargs)

    return response


# ---------------------------
# SET JWT COOKIES
# ---------------------------
def set_jwt_cookies(response, access_token, refresh_token, request=None):
    cookie_settings = cookie_settings_for_request(request) if request else get_cookie_settings()

    access_age = int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds())
    refresh_age = int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds())
    cookie_domain = getattr(settings, "COOKIE_DOMAIN", None)

    if cookie_domain:
        response.set_cookie("access_token", access_token, max_age=access_age, domain=cookie_domain, **cookie_settings)
        response.set_cookie("refresh_token", refresh_token, max_age=refresh_age, domain=cookie_domain, **cookie_settings)
    else:
        response.set_cookie("access_token", access_token, max_age=access_age, **cookie_settings)
        response.set_cookie("refresh_token", refresh_token, max_age=refresh_age, **cookie_settings)

    return response


# ---------------------------
# USER VIEW
# ---------------------------
@api_view(["GET", "PUT", "PATCH"])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([IsAuthenticated])
def user_view(request):
    user = request.user

    if request.method == "GET":
        return Response({
            "id": str(user.id),
            "first_name": user.first_name,
            "last_name": user.last_name,
            "full_name": user.full_name,
            "username": user.username,
            "email": user.email,
            "country": user.country,
            "state": user.state,
        })

    # ---- UPDATE PROFILE ----
    if request.method in ["PUT", "PATCH"]:
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        email = request.data.get("email")
        username = request.data.get("username")
        country = request.data.get("country")
        state = request.data.get("state")
        password = request.data.get("password")

        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if email is not None:
            user.email = email
        if username is not None:
            user.username = username
        if country is not None:
            user.country = country
        if state is not None:
            user.state = state
        if password:
            user.set_password(password)

        try:
            user.save()
        except IntegrityError as e:
            if "email" in str(e):
                return Response({"email": ["This email is already taken."]}, status=400)
            if "username" in str(e):
                return Response({"username": ["This username is already taken."]}, status=400)
            return Response({"detail": "Update failed."}, status=400)

        return Response({
            "id": str(user.id),
            "first_name": user.first_name,
            "last_name": user.last_name,
            "full_name": user.full_name,
            "username": user.username,
            "email": user.email,
            "country": user.country,
            "state": user.state,
        })


# ---------------------------
# CURRENT USER
# ---------------------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = CurrentUserSerializer(request.user, context={'request': request})
    return Response(serializer.data)


# ---------------------------
# GET CSRF
# ---------------------------
@api_view(["GET"])
@ensure_csrf_cookie
def get_csrf(request):
    token = csrf.get_token(request)
    return Response({"detail": "CSRF cookie set", "csrfToken": token}, status=200)
