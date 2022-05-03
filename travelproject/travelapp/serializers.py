from .models import *
from rest_framework.serializers import ModelSerializer


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id','name']


class AttractionTourSerializer(ModelSerializer):
    class Meta:
        model = Attraction
        fields = ['id','location']



class ToursTagSerializer(ModelSerializer):
    attraction = AttractionTourSerializer()
    class Meta:
        exclude = ['tag','customers','created_date','updated_date','note']
        model = Tour
