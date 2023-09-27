from django.conf.urls.static import static
from django.conf.urls import include
from django.contrib import admin
from django.conf import settings
from django.urls import path


urlpatterns = [
    path('', include('qcqualitycontrol.content.urls')),
    path('', include('qcqualitycontrol.core.urls')),
    path('admin/', admin.site.urls),
]


handler400 = "qcqualitycontrol.core.views.error_400_view"
handler403 = "qcqualitycontrol.core.views.error_403_view"
handler404 = "qcqualitycontrol.core.views.error_404_view"
handler500 = "qcqualitycontrol.core.views.error_500_view"


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)), ]
