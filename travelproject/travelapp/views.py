from django.core.mail import send_mail, EmailMessage
from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets, generics,permissions,status
from rest_framework.views import APIView
from .models import *
from .serializers import *
from .paginators import *
from rest_framework.response import Response
from rest_framework.decorators import action
from .perms import *
from decimal import Decimal
from datetime import datetime


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

class TourViewSet(viewsets.ViewSet,generics.ListAPIView,generics.RetrieveAPIView):
    queryset = Tour.objects.filter(active = True)
    serializer_class = TourSerializer
    pagination_class = TourPaginator
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
    @action(methods=['get'], detail=True, url_path='customers')
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

class BookTourViewSet(viewsets.ViewSet,generics.ListAPIView,generics.RetrieveAPIView,
                      generics.DestroyAPIView,generics.UpdateAPIView):
    queryset = BookTour.objects.all()
    serializer_class = BookTourSerializer
    # def get_permissions(self):
    #     if self.action in ['create']:
    #         return [permissions.IsAuthenticated()]
    #     return [OwnerPermisson()]
    def create(self, request):
        err_msg = None
        user_int = request.data.get('user')
        user = User.objects.get(pk = user_int)
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
    @action(methods=['get'], detail=True, url_path='total_price')
    def get_total_price(self, request, pk):
        book_tour =  self.get_object()
        tour = self.get_object().tour
        total_price = tour.price_for_children * book_tour.num_of_children + book_tour.num_of_adults * tour.price_for_adults
        return Response(data={'total-price':total_price},
                        status=status.HTTP_200_OK)
    @action(methods=['get'], detail=True, url_path='send_mail')
    def get_send_mail(self, request, pk):
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


class UserViewSet(viewsets.ViewSet,generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    @action(methods=['post'], url_path='reset_password', detail=False)
    def get_reset_password(self,request):
        pass

class SendMailAPIView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
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
    def get_payment_by_cash(self,request):
        pass
    @action(methods=['post'], url_path='payment_by_momo', detail=True)
    def get_payment_by_momo(self,request):
        pass
    @action(methods=['post'], url_path='payment_by_zalopay', detail=True)
    def get_payment_by_zalopay(self,request):
        pass
    #thanh toan xong phai gui mail
