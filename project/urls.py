from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from apps.main.views import landing_redirect

schema_view = get_schema_view(
   openapi.Info(
      title="Hospote Api V1",
      default_version='v1',
      description="Backend developer test by osw4l",
      contact=openapi.Contact(email="info@ponemus.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)

urlpatterns = [
    # path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('main/', include('apps.main.urls')),
    path('', landing_redirect)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)