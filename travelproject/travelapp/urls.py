from rest_framework import routers
from django.urls import path, include
from .admin import admin_site
from . import views

router = routers.DefaultRouter()
router.register(prefix="tags",viewset = views.TagViewSet,basename='tag')
router.register(prefix="attractions",viewset = views.AttractionViewSet,basename='attraction')
router.register(prefix="tours",viewset = views.TourViewSet,basename='tour')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin_site.urls),
]