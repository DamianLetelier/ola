from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('crud_Matias.urls')),  # Todas las rutas están en crud_Matias
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
