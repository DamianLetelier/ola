"""
URL configuration for Crud_Damian project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.http import HttpResponse
from Crud.views import landing

def simple_healthcheck(request):
    return HttpResponse("Healthy")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', simple_healthcheck, name='root-health'),  # 👈 esto responde 200 a "/"
    path('landing/', include('Crud.urls')),            # 👈 mueve la app a /landing/
    path('healthcheck/', simple_healthcheck, name='healthcheck'),
    path('matias/', include('crud_Matias.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
