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
        # request = self.context['request']
        # return request.build_absolute_uri(path)
        if obj.image:
            path = '{cloud_path}{image_name}'.format(cloud_path=cloud_path,image_name = obj.image)
            return path
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
        if obj.avatar:
            path = '{cloud_path}{image_name}'.format(cloud_path=cloud_path, image_name=obj.avatar)
            return path
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

class UserSerializer(ModelSerializer):
    avatar_path = serializers.SerializerMethodField(source='avatar')
    def get_avatar_path(self, obj):
        if obj.avatar:
            path = '{cloud_path}{image_name}'.format(cloud_path=cloud_path, image_name=obj.avatar)
            return  path
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'avatar', 'avatar_path']
        extra_kwargs = {
            'password': {
                'write_only': True
            }, 'avatar_path': {
                'read_only': True
            }, 'avatar': {
                'write_only': True
            }
        }
    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(user.password)
        user.save()
        return user
class TypeOfPaymentSerializer(ModelSerializer):
    class Meta:
        model = TypeOfPayment
        fields = ['payment_type']


class BillSerializer(ModelSerializer):
    payment_type = TypeOfPaymentSerializer()
    class Meta:
        model = Bill
        fields = '__all__'


class NewsSerializer(ModelSerializer):
    author = UserSerializer()
    class Meta:
        model = News
        fields = '__all__'

class CommentNewsSerializer(ModelSerializer):
    user = UserSerializer()
    class Meta:
        exclude = ['news']
        model = CommentNews

class CommentTourSerializer(ModelSerializer):
    user = UserSerializer()
    class Meta:
        exclude = ['tour']
        model = CommentTour


class CreateCommentTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentTour
        fields = ['id','content', 'tour', 'user']
        extra_kwargs = {
            'user': {
                'read_only': True
            }
        }


class CreateCommentNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentNews
        fields = ['id','content', 'news', 'user']
        extra_kwargs = {
            'user': {
                'read_only': True
            }
        }


class CreateRateNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ['id','star_rate', 'tour', 'user']
        extra_kwargs = {
            'user': {
                'read_only': True
            }
        }