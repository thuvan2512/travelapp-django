from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets, generics,permissions,status
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

class BookTourViewSet(viewsets.ViewSet,generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = BookTour.objects.all()
    serializer_class = BookTourSerializer