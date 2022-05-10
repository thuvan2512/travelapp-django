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
router.register(prefix="type_of_payment",viewset = views.TypeOfPaymentViewSet,basename='type_of_payment')
router.register(prefix="news",viewset = views.NewsViewSet,basename='news')
router.register(prefix="comment_tour",viewset = views.CommentTourViewSet,basename='comment_tour')
router.register(prefix="comment_news",viewset = views.CommentNewsViewSet,basename='comment_news')
router.register(prefix="rate",viewset = views.RateViewSet,basename='rate')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin_site.urls),
    path('send_mail/', views.SendMailAPIView.as_view(), name='send_mail'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('revenue_stats/month/', views.RevenueStatsMonthView.as_view(), name='revenue_stats_month'),
    path('revenue_stats/year/', views.RevenueStatsYearView.as_view(), name='revenue_stats_year'),
    path('revenue_stats/quarterly/', views.RevenueStatsQuarterlyView.as_view(), name='revenue_stats_quarterly'),
]