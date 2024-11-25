from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

import images
from Booksmarks import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('images/', include('images.urls', namespace='images')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)