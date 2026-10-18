from django.contrib import admin
from django.urls import include, path
from core.views import admin_login_api

urlpatterns = [
    path("admin/", admin.site.urls),
    path('admin/login/', admin_login_api, name='admin_login_api'),
    path("api/", include("core.urls")),
]