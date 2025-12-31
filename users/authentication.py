import logging
from django.conf import settings
from rest_framework import authentication, exceptions
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)

class CookieJWTAuthentication(authentication.BaseAuthentication):
    """
    Authenticate user using JWT stored in HttpOnly cookies.
    Works for both local development and production cross-origin setups.
    """

    def authenticate(self, request):
        # Try to get the JWT from the cookie
        token = request.COOKIES.get("access_token")

        # For development, token might also be in Authorization header
        if settings.DEBUG and not token:
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            logger.debug(f"No access_token found. Request path: {request.path}")
            return None

        try:
            # Decode the JWT
            backend = TokenBackend(
                algorithm=settings.SIMPLE_JWT.get("ALGORITHM", "HS256"),
                signing_key=settings.SIMPLE_JWT.get("SIGNING_KEY", settings.SECRET_KEY),
            )
            decoded = backend.decode(token, verify=True)
        except (TokenError, InvalidToken) as e:
            logger.warning(f"Invalid or expired token. Error: {str(e)}")
            raise exceptions.AuthenticationFailed("Invalid or expired token")

        user_id = decoded.get("user_id")
        if not user_id:
            logger.warning(f"Token missing user_id. Decoded payload: {decoded}")
            raise exceptions.AuthenticationFailed("Token missing user_id")

        # Retrieve user
        User = get_user_model()
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            logger.warning(f"User with ID {user_id} not found")
            raise exceptions.AuthenticationFailed("User not found")

        logger.debug(f"Authenticated user {user.username} (ID: {user.id})")
        return (user, None)

    def enforce_csrf(self, request):
        """
        Overridden to bypass CSRF validation for JWT in cookies.
        Prevents 403 errors when using JWT instead of session auth.
        """
        return  # no CSRF check needed