from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('courses.urls')),  # This will make the home page accessible at the root URL
    path('admin/', admin.site.urls),
    path('courses/', include('courses.urls')),  # Keep this for backward compatibility
    path('reviews/', include('reviews.urls')),  # Add the reviews app URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
