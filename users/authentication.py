import logging
from typing import Optional, Tuple
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication, exceptions
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.contrib.auth.models import AbstractBaseUser

logger = logging.getLogger(__name__)
User = get_user_model()


class CookieJWTAuthentication(authentication.BaseAuthentication):
    """
    Authenticate users via JWT stored in HttpOnly cookies.
    - Uses 'access_token' cookie primarily.
    - Falls back to Authorization header only in DEBUG mode.
    - Strictly authenticates users by email.
    - Bypasses CSRF (use with SameSite cookies for security).
    """

    def authenticate(self, request) -> Optional[Tuple[AbstractBaseUser, None]]:
        token = self._get_token(request)

        if not token:
            logger.debug(f"No JWT found. Path: {request.path}")
            return None  # Not raising here so DRF can continue other auths

        decoded = self._decode_token(token)

        user_id = decoded.get("user_id")
        if not user_id:
            logger.warning(f"JWT missing user_id. Payload: {decoded}")
            raise exceptions.AuthenticationFailed("Invalid token: missing user identifier")

        user = self._get_user(user_id)
        logger.debug(f"Authenticated user {user.email} (ID: {user.id})")
        return (user, None)

    # --------------------------------------
    # Helper methods
    # --------------------------------------
    def _get_token(self, request) -> Optional[str]:
        """
        Retrieves JWT token from cookie or header (DEBUG only).
        """
        token = request.COOKIES.get("access_token")
        if not token and settings.DEBUG:
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
        return token

    def _decode_token(self, token: str) -> dict:
        """
        Decodes the JWT token and verifies signature & expiry.
        """
        algorithm = settings.SIMPLE_JWT.get("ALGORITHM", "HS256")
        signing_key = settings.SIMPLE_JWT.get("SIGNING_KEY") or settings.SECRET_KEY

        backend = TokenBackend(algorithm=algorithm, signing_key=signing_key)

        try:
            return backend.decode(token, verify=True)
        except (TokenError, InvalidToken) as e:
            logger.warning(f"Invalid or expired JWT: {str(e)}")
            raise exceptions.AuthenticationFailed("Invalid or expired token")

    def _get_user(self, user_id: str) -> AbstractBaseUser:
        """
        Retrieves user by ID. Raises AuthenticationFailed if not found or inactive.
        """
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            logger.warning(f"User with ID {user_id} not found")
            raise exceptions.AuthenticationFailed("User not found")

        if not user.is_active:
            logger.warning(f"Inactive user attempted authentication: {user.email}")
            raise exceptions.AuthenticationFailed("User account is inactive")

        return user

    # --------------------------------------
    # CSRF override
    # --------------------------------------
    def enforce_csrf(self, request) -> None:
        """
        Bypasses CSRF checks since JWT is stateless and stored in HttpOnly cookies.
        Ensure SameSite=Strict/Lax for cookie security.
        """
        return