from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bill/', include('bill.api.urls')),
    path('building/', include('building.api.urls'))
] + debug_toolbar_urls()
