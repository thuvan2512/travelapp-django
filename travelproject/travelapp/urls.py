from rest_framework import routers
from django.urls import path, include

router = routers.DefaultRouter()
from .admin import admin_site
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin_site.urls),
]