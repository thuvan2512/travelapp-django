from django.shortcuts import render
from rest_framework import viewsets, generics,permissions,status
from .models import *
from .serializers import *
from .paginators import *
from rest_framework.response import Response
from rest_framework.decorators import action
from .perms import *



class TagViewSet(viewsets.ViewSet,generics.RetrieveAPIView,generics.ListAPIView):
    queryset = Tag.objects.all().order_by('id')
    serializer_class = TagSerializer
    pagination_class = TagPaginator
    permission_classes = [permissions.AllowAny]
    # def get_permissions(self):
    #     if self.action in ['retrieve']:
    #         return [AdminPermission()]
    #     return [permissions.AllowAny()]
    @action(methods=['get'], detail=True, url_path='tours')
    def get_tours(self, request, pk):
        tours = self.get_object().tours
        return Response(data=ToursTagSerializer(tours, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)