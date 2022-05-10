from django.core.mail import send_mail, EmailMessage
from django.db.models import Q, Count, Sum
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics,permissions,status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from .models import *
from .serializers import *
from .paginators import *
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from django.contrib.auth import login, logout
from django.contrib.auth import  authenticate
from .perms import *
from decimal import Decimal
from datetime import datetime,date
import random,hashlib
from .utils import *



class TagViewSet(viewsets.ViewSet,generics.RetrieveAPIView,generics.ListAPIView):
    queryset = Tag.objects.all().order_by('id')
    serializer_class = TagSerializer
    pagination_class = TagPaginator
    permission_classes = [permissions.AllowAny]
    def get_queryset(self):
        query = self.queryset

        kw = self.request.query_params.get('kw')
        if kw:
            query = query.filter(name__icontains=kw)
        return query
    # def get_permissions(self):
    #     if self.action in ['retrieve']:
    #         return [AdminPermission()]
    #     return [permissions.AllowAny()]
    @action(methods=['get'], detail=True, url_path='tours')
    def get_tours(self, request, pk):
        tours = self.get_object().tours
        return Response(data=TourSerializer(tours, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)


class AttractionViewSet(viewsets.ViewSet,generics.ListAPIView,generics.RetrieveAPIView):
    queryset = Attraction.objects.filter(active = True)
    serializer_class = AttractionSerializer
    pagination_class = AttractionPaginator
    permission_classes = [permissions.AllowAny]
    def get_queryset(self):
        query = self.queryset

        kw = self.request.query_params.get('kw')
        if kw:
            query = query.filter(location__icontains=kw)
        return query

    @action(methods=['get'], detail=True, url_path='tours')
    def get_tours(self, request, pk):
        tours = self.get_object().tours
        return Response(data=TourSerializer(tours, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)
        # paginator = pagination.PageNumberPagination()
        # pagination.PageNumberPagination.page_size = 2
        # tours = paginator.paginate_queryset(tours, request)
        # return paginator.get_paginated_response(TourSerializer(tours, many=True).data)

class TourViewSet(viewsets.ViewSet,generics.ListAPIView,generics.RetrieveAPIView):
    queryset = Tour.objects.filter(active = True)
    serializer_class = TourSerializer
    pagination_class = TourPaginator
    permission_classes = [permissions.AllowAny]
    def get_queryset(self):
        query = self.queryset
        kw = self.request.query_params.get('kw')
        price_from = self.request.query_params.get('price_from')
        price_to = self.request.query_params.get('price_to')
        departure_str = self.request.query_params.get('departure_date')
        if kw:
            query = query.filter(name__icontains=kw)
        if departure_str:
            try:
                departure_date = datetime.strptime(departure_str, "%Y-%m-%d").date()
            except:
                query = query.none()
            else:
                query = query.filter(departure_date__exact=departure_date)
        if price_to or price_from:
            if price_to and price_from:
                query = query.filter(Q(price_for_adults__gte=Decimal(price_from),price_for_adults__lte=Decimal(price_to)) |\
                                     Q(price_for_children__gte=Decimal(price_from),price_for_children__lte=Decimal(price_to)))
            elif price_from:
                query = query.filter(Q(price_for_adults__gte=Decimal(price_from))|\
                                     Q(price_for_children__gte=Decimal(price_from)))
            else:
                query = query.filter(Q(price_for_adults__lte=Decimal(price_to)) | \
                                     Q(price_for_children__lte=Decimal(price_to)))
        return query

    @action(methods=['get'], detail=True, url_path='customers',permission_classes = [permissions.IsAuthenticated])
    def get_customers(self, request, pk):
        customers = self.get_object().customers
        return Response(data=CustomerSerializer(customers, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='tags')
    def get_tags(self, request, pk):
        tags = self.get_object().tag
        return Response(data=TagSerializer(tags, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='images')
    def get_images(self, request, pk):
        images = self.get_object().images
        return Response(data=ImageTourSerializer(images, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)
    @action(methods=['get'], url_path='comments', detail=True,permission_classes=[permissions.AllowAny])
    def get_comments(self, request, pk):
        tour = self.get_object()
        comments = tour.comments
        comments = comments.select_related('user')
        paginator = pagination.PageNumberPagination()
        pagination.PageNumberPagination.page_size = 10
        comments = paginator.paginate_queryset(comments, request)
        return paginator.get_paginated_response(CommentTourSerializer(comments, many=True).data)

    @action(methods=['get'], url_path='rate', detail=True,permission_classes=[permissions.AllowAny])
    def get_rate(self, request, pk):
        tour = self.get_object()
        rate = tour.rate
        rate = rate.select_related('user')
        paginator = pagination.PageNumberPagination()
        pagination.PageNumberPagination.page_size = 1
        rate = paginator.paginate_queryset(rate, request)
        return paginator.get_paginated_response(RateSerializer(rate, many=True).data)


class BookTourViewSet(viewsets.ViewSet,generics.ListAPIView,generics.RetrieveAPIView,
                      generics.DestroyAPIView,generics.UpdateAPIView):
    queryset = BookTour.objects.all()
    serializer_class = BookTourSerializer
    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAuthenticated()]
        return [OwnerPermisson()]
    def create(self, request):
        err_msg = None
        # user = User.objects.get(pk = request.data.get('user'))
        user = request.user
        tour = Tour.objects.get(pk = request.data.get('tour'))
        check_time = tour.departure_date <= datetime.now().date()
        if user:
            if not user.email:
                return Response(data={
                    'error_msg':'Users who do not have an email, please add email information before booking'
                },status= status.HTTP_400_BAD_REQUEST)
            elif check_time:
                return Response(data={
                    'error_msg': 'Expired tour booking'
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                num_of_children = request.data.get('num_of_children')
                num_of_adults = request.data.get('num_of_adults')
                try:
                    book_tour = BookTour.objects.create(num_of_adults = num_of_adults,num_of_children = num_of_children,user = user,tour = tour)
                    serializers = BookTourSerializer(book_tour)
                    bill = Bill.objects.create(book_tour = book_tour)
                    total_price = tour.price_for_children * float(num_of_children) + float(num_of_adults) * tour.price_for_adults
                    bill.total_price = total_price
                    bill.save()
                    return Response(data=serializers.data, status=status.HTTP_201_CREATED)
                except Exception as e:
                    err_msg = e.__str__()
                return Response(data={
                    'error_msg': err_msg
                },status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True, url_path='total_price',permission_classes = [permissions.IsAuthenticated])
    def get_total_price(self, request, pk):
        book_tour =  self.get_object()
        tour = self.get_object().tour
        total_price = tour.price_for_children * book_tour.num_of_children + book_tour.num_of_adults * tour.price_for_adults
        return Response(data={'total-price':total_price},
                        status=status.HTTP_200_OK)
    @action(methods=['get'], detail=True, url_path='send_mail',permission_classes = [permissions.IsAuthenticated])
    def send_mail(self, request, pk):
        book_tour = self.get_object()
        error_msg = None
        if book_tour:
            if not book_tour.send_mail:
                user = book_tour.user
                if user.email:
                    tour = book_tour.tour
                    total_price = tour.price_for_children * book_tour.num_of_children + book_tour.num_of_adults * tour.price_for_adults
                    email = user.email
                    subject = "Chào mừng bạn đến với dịch vụ của Travel Agency OU"
                    try:
                        content = """
Chào {0}
    Hệ thống đã ghi nhận đơn đặt tour của bạn!!!
    Chi tiết:
        Mã đơn: {1}
        Tên khách hàng: {2}
        Tên tour: {3}
        Ngày khởi hành:{4}
        Số lượng người lớn: {5}
        Số lượng trẻ em: {6}
        =====================
        Tổng tiền cần thanh toán: {7:,.0f} VND
Vui lòng thanh toán trước thời điểm khởi hành. Nếu quá hạn mà chưa thanh toán thì đơn đặt tour của quý khách sẽ bị hủy.
Travel Agency OU xin chân thành cám ơn.

Mọi thắc mắc và yêu cầu hỗ trợ xin gửi về địa chỉ travel.agency.ou@gmail.com.
                        """.format(user.username,
                                   book_tour.pk,user.first_name +" " + user.last_name,
                                   tour.name,
                                   tour.departure_date,
                                   book_tour.num_of_adults,
                                   book_tour.num_of_children,
                                   total_price)
                        if email and subject and content:
                            send_email = EmailMessage(subject, content, to=[email])
                            send_email.send()
                        else:
                            error_msg = "Send mail failed !!!"
                    except:
                        error_msg = 'Email content error. Check additional customer and tour information'
                else:
                    error_msg = "No customer email information !!!"
            else:
                error_msg = "Email has been sent before!!!"
        if not error_msg:
            book_tour.send_mail = True
            book_tour.save()
            return Response(data={
                'status': 'Send mail successfully',
                'to': email,
                'subject': subject,
                'content': content
            }, status=status.HTTP_200_OK)
        return Response(data={'error_msg': error_msg},
                        status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ViewSet,generics.CreateAPIView,generics.UpdateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    def get_permissions(self):
        if self.action in ['partial_update','update']:
            return [UserOwnerPermisson()]
        return [permissions.AllowAny()]

    @action(methods=['post'], url_path='reset_password', detail= False)
    def reset_password(self,request):
        email = request.data.get('email')
        if email:
            user = User.objects.filter(email = email).first()
            if user:
                code = random_for_confirm_code()
                CodeConfirm.objects.update_or_create(user = user, defaults={
                    'code': str(hashlib.sha256(str(code).encode("utf-8")).hexdigest())
                })
                subject = "Xác nhận reset mật khẩu trên hệ thống Travel Agency OU"
                content = """
                Chào {0}
                Chúng tôi đã nhận yêu cầu reset mật khẩu cho tài khoản của bạn.
                Mã xác nhận cho tài khoản của bạn là: {1}
                Nếu xác nhận thì đây cũng chính là mật khẩu mới của bạn.
                Mọi thắc mắc và yêu cầu hỗ trợ xin gửi về địa chỉ travel.agency.ou@gmail.com.
                                        """.format(user.username,code)
                send_email = EmailMessage(subject, content, to=[email])
                send_email.send()
                return Response(data={"message": "Send email confirm successfully"}, status=status.HTTP_200_OK)
            else:
                return Response(data={"error_message":"User not found"},status = status.HTTP_404_NOT_FOUND)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], url_path='reset_password/confirm', detail=False)
    def confirm(self,request):
        confirm_code = request.data.get('confirm_code')
        email = request.data.get('email')
        if email and confirm_code:
            user = User.objects.filter(email=email).first()
            if user:
                code_obj = CodeConfirm.objects.filter(user = user).first()
                if code_obj:
                    if str(code_obj.code).__eq__(str(hashlib.sha256(str(confirm_code).encode("utf-8")).hexdigest())):
                        user.set_password(str(confirm_code))
                        user.save()
                        code_obj.delete()
                        return Response(data={"message":"Confirm successfully"},status = status.HTTP_200_OK)
                    else:
                        return Response(data={"error_message":"Wrong code"},status = status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(data={"error_message":"Confirm code error"},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data={"error_message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SendMailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        email = request.data.get('email')
        subject = request.data.get('subject')
        content = request.data.get('content')
        error_msg = None
        if email and subject and content:
            send_email = EmailMessage(subject, content, to=[email])
            send_email.send()
        else:
            error_msg = "Send mail failed !!!"
        if not error_msg:
            return Response(data={
                'status': 'Send mail successfully',
                'to': email,
                'subject':subject,
                'content':content
            },status=status.HTTP_200_OK)
        return Response(data={'error_msg': error_msg},
                            status=status.HTTP_400_BAD_REQUEST)

class BillViewSet(viewsets.ViewSet,generics.ListAPIView,generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BillSerializer
    queryset = Bill.objects.filter(active = True)
    def get_queryset(self):
        bills = self.queryset
        bills = bills.select_related('payment_type')
        return bills
    # def list(self, request):
    #     bills = Bill.objects.filter(active=True).select_related('payment_type')
    #     serializer = BillSerializer(bills, many=True)
    #     return Response(data=serializer.data,status = status.HTTP_200_OK)
    # def retrieve(self, request, pk):
    #     try:
    #         bill = Bill.objects.get(pk=pk)
    #         return Response(data=BillSerializer(bill).data, status=status.HTTP_200_OK)
    #     except Bill.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    @action(methods=['post'], url_path='payment_by_cash', detail=True)
    def payment_by_cash(self,request):
        pass
    @action(methods=['post'], url_path='payment_by_momo', detail=True)
    def payment_by_momo(self,request):
        pass
    @action(methods=['post'], url_path='payment_by_zalopay', detail=True)
    def payment_by_zalopay(self,request):
        pass
    #thanh toan xong phai gui mail


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(data={'message':"Login successfully"},status = status.HTTP_202_ACCEPTED)
        else:
            return Response(data={'error_msg':"Invalid user"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def logout_view(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)


class NewsViewSet(viewsets.ViewSet,generics.ListAPIView,generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    pagination_class = NewsPaginator
    serializer_class = NewsSerializer
    queryset = News.objects.filter(active = True)
    def get_queryset(self):
        news = self.queryset
        news = news.select_related('author')
        kw = self.request.query_params.get('kw')
        if kw:
            news = news.filter(title__icontains=kw)
        return news

    @action(methods=['post'], url_path='like', detail=True,permission_classes = [permissions.IsAuthenticated])
    def like(self, request, pk):
        news = self.get_object()
        user = request.user
        like, _ = Like.objects.get_or_create(news = news, user=user)
        like.state = not like.state
        like.save()
        return Response(status=status.HTTP_201_CREATED)

    @action(methods=['get'], url_path='count_like', detail=True, permission_classes=[permissions.AllowAny])
    def count_like(self, request, pk):
        news = self.get_object()
        total_like = news.likes.filter(state = True).count()
        return Response(data={
            "total_like":total_like
        },status=status.HTTP_200_OK)

    @action(methods=['get'], url_path='comments', detail=True,permission_classes=[permissions.AllowAny])
    def get_comments(self, request, pk):
        news = self.get_object()
        comments = news.comments
        comments = comments.select_related('user')
        paginator = pagination.PageNumberPagination()
        pagination.PageNumberPagination.page_size = 10
        comments = paginator.paginate_queryset(comments, request)
        return paginator.get_paginated_response(CommentNewsSerializer(comments, many=True).data)


class TypeOfPaymentViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = TypeOfPaymentSerializer
    pagination_class = None
    queryset = TypeOfPayment.objects.all()


class CommentTourViewSet(viewsets.ViewSet,generics.UpdateAPIView,generics.DestroyAPIView):
    queryset = CommentTour.objects.all()
    serializer_class = CreateCommentTourSerializer
    def get_permissions(self):
        if self.action in ['partial_update','update', 'destroy']:
            return [OwnerPermisson()]
        return [permissions.IsAuthenticated()]
    def create(self, request):
        user = request.user
        if user:
            try:
                content = request.data.get('content')
                tour = Tour.objects.get(pk=request.data.get('tour'))
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if tour and content:
                comment_tour = CommentTour.objects.create(user = user,tour = tour,content = content)
                return Response(data=CreateCommentTourSerializer(comment_tour).data,status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"error_message":"User not found"},status = status.HTTP_400_BAD_REQUEST)


class CommentNewsViewSet(viewsets.ViewSet,generics.UpdateAPIView,generics.DestroyAPIView):
    queryset = CommentNews.objects.all()
    serializer_class = CreateCommentNewsSerializer
    def get_permissions(self):
        if self.action in ['partial_update','update', 'destroy']:
            return [OwnerPermisson()]
        return [permissions.IsAuthenticated()]
    def create(self, request):
        user = request.user
        if user:
            try:
                content = request.data.get('content')
                news = News.objects.get(pk=request.data.get('news'))
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if news and content:
                comment_news = CommentNews.objects.create(user = user,news = news,content = content)
                return Response(data=CreateCommentNewsSerializer(comment_news).data,status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"error_message":"User not found"},status = status.HTTP_400_BAD_REQUEST)


class RateViewSet(viewsets.ViewSet,generics.UpdateAPIView,generics.DestroyAPIView):
    queryset = Rate.objects.all()
    serializer_class = CreateRateSerializer
    def get_permissions(self):
        if self.action in ['partial_update','update', 'destroy']:
            return [OwnerPermisson()]
        return [permissions.IsAuthenticated()]
    def create(self, request):
        user = request.user
        if user:
            try:
                star_rate = request.data.get('star_rate')
                tour = Tour.objects.get(pk=request.data.get('tour'))
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if tour and star_rate:
                r, _ = Rate.objects.get_or_create(tour = tour, user=user)
                r.star_rate = star_rate
                r.save()
                return Response(data=CreateRateSerializer(r).data,status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"error_message":"User not found"},status = status.HTTP_400_BAD_REQUEST)


class RevenueStatsMonthView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self,request):
        revenue_stats_month_str = request.data.get('revenue_stats_month')
        try:
            revenue_stats_month = datetime.strptime(revenue_stats_month_str, '%Y-%m')
        except:
            return Response(data={"error_msg": "cannot be left blank"},
                        status=status.HTTP_400_BAD_REQUEST)
        else:
            if revenue_stats_month:
                count_book_tour = BookTour.objects.filter(created_date__year=revenue_stats_month.year,created_date__month=revenue_stats_month.month).count()
                count_bill_paid = Bill.objects.filter(payment_state=True, created_date__year=revenue_stats_month.year,created_date__month=revenue_stats_month.month).count()
                total_revenue = Bill.objects.filter(payment_state=True, created_date__year=revenue_stats_month.year,created_date__month=revenue_stats_month.month). \
                    aggregate(sum=Sum('total_price'))['sum']
                return Response(data={
                    "count_book_tour":count_book_tour,
                    "count_bill_paid": count_bill_paid,
                    "total_revenue":total_revenue,
                }, status=status.HTTP_200_OK)
            return Response(data={"error_msg": "revenue_stats_month not found"},
                            status=status.HTTP_400_BAD_REQUEST)


class RevenueStatsYearView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        revenue_stats_year = request.data.get('revenue_stats_year')
        try:
            revenue_stats_year = int(revenue_stats_year)
        except:
            return Response(data={"error_msg": "cannot be left blank"},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            if revenue_stats_year:
                count_book_tour = BookTour.objects.filter(created_date__year=revenue_stats_year).count()
                count_bill_paid = Bill.objects.filter(payment_state=True, created_date__year=revenue_stats_year).count()
                total_revenue = Bill.objects.filter(payment_state=True, created_date__year=revenue_stats_year). \
                    aggregate(sum=Sum('total_price'))['sum']
                return Response(data={
                    "count_book_tour": count_book_tour,
                    "count_bill_paid": count_bill_paid,
                    "total_revenue": total_revenue,
                }, status=status.HTTP_200_OK)
            return Response(data={"error_msg": "revenue_stats_year not found"},
                            status=status.HTTP_400_BAD_REQUEST)


class RevenueStatsQuarterlyView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self,request):
        revenue_stats_from_str = request.data.get('revenue_stats_from')
        revenue_stats_to_str = request.data.get('revenue_stats_to')
        try:
            revenue_stats_from = datetime.strptime(revenue_stats_from_str, '%Y-%m-%d')
            revenue_stats_to = datetime.strptime(revenue_stats_to_str, '%Y-%m-%d')
        except:
            return Response(data={"error_msg": "cannot be left blank"},
                        status=status.HTTP_400_BAD_REQUEST)
        else:
            if revenue_stats_from and revenue_stats_to:
                count_book_tour = BookTour.objects.filter(created_date__gte = revenue_stats_from,created_date__lte=revenue_stats_to).count()
                count_bill_paid = Bill.objects.filter(payment_state=True, created_date__gte = revenue_stats_from,created_date__lte=revenue_stats_to).count()
                total_revenue = Bill.objects.filter(payment_state=True, created_date__gte = revenue_stats_from,created_date__lte=revenue_stats_to). \
                    aggregate(sum=Sum('total_price'))['sum']
                return Response(data={
                    "count_book_tour":count_book_tour,
                    "count_bill_paid": count_bill_paid,
                    "total_revenue":total_revenue,
                }, status=status.HTTP_200_OK)
            return Response(data={"error_msg": "revenue_stats_quarterly not found"},
                            status=status.HTTP_400_BAD_REQUEST)
