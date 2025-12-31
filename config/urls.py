"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
import os
# from core.admin_dashboard import admin_dashboard

admin_url = os.environ.get("DJANGO_ADMIN_URL", "secret-cave-102")

def root_view(request):
    return JsonResponse({"message": "API is running"})

urlpatterns = [
    path(f"{admin_url}/", admin.site.urls),
    # path(f"{admin_url}/dashboard/", admin_dashboard, name="admin-dashboard"),
    # path("api/", include("core.urls")),
    path("api/", include("users.urls")),
    # path("api/", include("wallet.urls")),
    # path("api/", include("transactions.urls")),
    # path("api/", include("plans.urls")),
    # path("api/", include("support.urls")),
    # path("api/", include("notifications.urls")),
    # path("api/", include("landing.urls")),
    path("", root_view), # Minimal root endpoint
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)