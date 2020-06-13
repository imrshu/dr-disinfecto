from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (password_reset, password_reset_done, 
password_reset_confirm, password_reset_complete
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('product.urls', namespace = 'product')),
    path('password_reset', password_reset, name='password_reset'),
    path('password_reset_done', password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>', password_reset_confirm, name='password_reset_confirm'),
    path('reset/done', password_reset_complete, name='password_reset_complete')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
