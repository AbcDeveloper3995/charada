"""charada URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings

from apps.utils import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.usuario.urls')),
    path('charada/', include('apps.charada.urls')),
    path('', include('pwa.urls')),
]

handler_400 = badRequest403
handler_403 = permissionDenied403
handler_404 = pageNotFound404
handler_500 = internalError500

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
