from django.conf import settings

from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)

from rest_framework.response import Response


# ---------------------------
# PING
# ---------------------------
@api_view(["GET"])
def ping(request):
    return Response({"message": "pong"})