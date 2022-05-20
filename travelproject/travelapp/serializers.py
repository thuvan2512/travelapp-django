from rest_framework.exceptions import AuthenticationFailed
from .register import register_social_user
from . import cloud_path, google, facebook
from django.conf import settings
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


class AttractionCompactSerializer(ModelSerializer):
    class Meta:
        model = Attraction
        fields = ['location']


class TourSerializer(ModelSerializer):
    attraction = AttractionCompactSerializer()
    image_path = serializers.SerializerMethodField(source='image')
    def get_image_path(self, obj):
        if obj.image:
            path = '{cloud_path}{image_name}'.format(cloud_path=cloud_path, image_name=obj.image)
            return path
    class Meta:
        model = Tour
        exclude = ['customers','tag','image']
        extra_kwargs = {
            'image_path': {
                'read_only': True
            },
        }


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

class CreateBookTourSerializer(ModelSerializer):
    class Meta:
        model = BookTour
        fields = ["num_of_adults","num_of_children","user","tour"]


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
        user.is_customer = True
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
    image_path = serializers.SerializerMethodField(source='image')
    def get_image_path(self, obj):
        if obj.image:
            path = '{cloud_path}{image_name}'.format(cloud_path=cloud_path, image_name=obj.image)
            return path
    class Meta:
        model = News
        fields = ['title','author','image_path','content']
        extra_kwargs = {
            'image_path': {
                'read_only': True
            },
        }

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


class RateSerializer(ModelSerializer):
    user = UserSerializer()
    class Meta:
        exclude = ['tour']
        model = Rate


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


class CreateRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ['id','star_rate', 'tour', 'user']
        extra_kwargs = {
            'user': {
                'read_only': True
            }
        }


class NewsViewSerializer(ModelSerializer):
    class Meta:
        model = NewsView
        fields = ['news','views', 'updated_date']




class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()
    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        if user_data['aud'] != settings.GOOGLE_CLIENT_ID:
            raise AuthenticationFailed('we cannot authenticate for you!!!')
        email = user_data['email']
        name = user_data['email']
        provider = 'google'

        return register_social_user(
            provider=provider, email=email, name=name)



class FacebookSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()
    def validate_auth_token(self, auth_token):
        user_data = facebook.Facebook.validate(auth_token)

        try:
        # user_id = user_data['id']
            email = user_data['email']
            name = user_data['name']
            provider = 'facebook'
            return register_social_user(
                provider=provider,
                # user_id=user_id,
                email=email,
                name=name
            )
        except Exception:

            raise serializers.ValidationError(
                'The token  is invalid or expired. Please login again.'
            )

