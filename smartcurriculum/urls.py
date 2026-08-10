from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', __import__('django.contrib.admin', fromlist=['site']).site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('attendance.urls')),
    path('timetable/', include('timetable.urls')),
    path('analytics/', include('analytics.urls')),
    path('api/', include('attendance.api_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
