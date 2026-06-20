
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("products/", include("products.urls")),
    #path('',include('pages.urls')),
    path('account/',include('Account.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
