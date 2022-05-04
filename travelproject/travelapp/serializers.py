from . import cloud_path
from .models import *
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class AttractionSerializer(ModelSerializer):
    class Meta:
        model = Attraction
        fields = '__all__'


class ImageTourSerializer(ModelSerializer):
    image_path = serializers.SerializerMethodField(source='image')
    def get_image_path(self, obj):
        request = self.context['request']
        if obj.image:
            path = '{cloud_path}{image_name}'.format(cloud_path=cloud_path,image_name = obj.image)
            return request.build_absolute_uri(path)
    class Meta:
        model = ImageTour
        fields = ['image_path','descriptions']
        extra_kwargs = {
            'image_path': {
                'read_only': True
            },
        }


class TourSerializer(ModelSerializer):
    class Meta:
        model = Tour
        exclude = ['customers','tag']


class CustomerSerializer(ModelSerializer):
    avatar_path = serializers.SerializerMethodField(source='avatar')
    def get_avatar_path(self, obj):
        request = self.context['request']
        if obj.avatar:
            path = '{cloud_path}{image_name}'.format(cloud_path=cloud_path, image_name=obj.avatar)
            return request.build_absolute_uri(path)
    class Meta:
        model = User
        fields = ['avatar_path','username','first_name','last_name','date_of_birth','phone','email']
        extra_kwargs = {
            'avatar_path': {
                'read_only': True
            },
        }
class BookTourSerializer(ModelSerializer):
    class Meta:
        model = BookTour
        fields = '__all__'