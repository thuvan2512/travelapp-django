from rest_framework import routers
from django.urls import path, include
from .admin import admin_site
from . import views

router = routers.DefaultRouter()
router.register(prefix="tags",viewset = views.TagViewSet,basename='tag')
router.register(prefix="attractions",viewset = views.AttractionViewSet,basename='attraction')
router.register(prefix="tours",viewset = views.TourViewSet,basename='tour')
router.register(prefix="book_tours",viewset = views.BookTourViewSet,basename='book_tour')
router.register(prefix="users",viewset = views.UserViewSet,basename='user')
router.register(prefix="bills",viewset = views.BillViewSet,basename='bill')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin_site.urls),
    path('send_mail/', views.SendMailAPIView.as_view(), name='send-mail'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]