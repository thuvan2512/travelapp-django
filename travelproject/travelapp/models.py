from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import  CloudinaryField
from ckeditor.fields import RichTextField



class Gender(models.Model):
    gender_type = models.CharField(max_length = 50, null = False)
    def __str__(self):
        return self.gender_type


class User(AbstractUser):
    gender = models.ForeignKey('Gender',related_name='users',null= True,on_delete=models.SET_NULL)
    date_of_birth = models.DateField(null=True)
    avatar = CloudinaryField('avatar',default = '')
    is_customer = models.BooleanField(default= False,verbose_name='Customer status')
    home_town = models.CharField(max_length=50,null= True, blank= True)
    phone = models.CharField(max_length=10,null= True, blank= True)


class ModelBase(models.Model):
    active = models.BooleanField(default = True)
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)
    class Meta:
        abstract = True


class ImageTour(ModelBase):
    image = CloudinaryField('image',default = '')
    descriptions = models.CharField(max_length = 255,null = True)
    tour_info = models.ForeignKey('TourInfo', on_delete = models.CASCADE, related_name = 'images',null=True)
    class Meta:
        verbose_name = 'Image of tour'



class News(ModelBase):
    title = models.CharField(max_length = 50, default="none")
    content = RichTextField(null=True)
    author = models.ForeignKey('User', on_delete = models.SET_NULL, related_name = 'list_news', null = True)
    class Meta:
        verbose_name = 'New'

class Tour(ModelBase):
    name = models.CharField(max_length=100,null= False, default="none")
    price_for_adults = models.FloatField(default = 0)
    price_for_children = models.FloatField(default = 0)
    departure_date = models.DateField(null = True)
    end_date = models.DateField(null=True)
    tour_info = models.ForeignKey('TourInfo',on_delete=models.CASCADE,related_name='tours')
    customers = models.ManyToManyField('User', through= 'BookTour',related_name='tours')
    def __str__(self):
        return self.name


class TourInfo(ModelBase):
    location = models.CharField(max_length = 50, default="none")
    description = RichTextField(null=True)
    def __str__(self):
        return self.location
    class Meta:
        verbose_name = 'Tour information'


class BookTour(ModelBase):
    user = models.ForeignKey('User',on_delete=models.CASCADE)
    tour = models.ForeignKey('Tour',on_delete=models.CASCADE)
    num_of_adults = models.IntegerField(default=0)
    num_of_children = models.IntegerField(default=0)


class ActionBase(models.Model):
    user =  models.ForeignKey('User', on_delete=models.CASCADE)
    class Meta:
        abstract = True

class CommentBase(ActionBase):
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)
    content = models.CharField(max_length=255,blank= True)
    class Meta:
        abstract = True


class Like(ActionBase):
    state = models.BooleanField(default= True)
    news = models.ForeignKey('News', on_delete=models.CASCADE, related_name='likes',null= True)


class CommentNews(CommentBase):
    news = models.ForeignKey('News',on_delete=models.CASCADE,related_name='comments',null= True)


class CommentTour(CommentBase):
    tour = models.ForeignKey('Tour',on_delete=models.CASCADE,related_name='comments',null= True)


class Rate(ActionBase):
    star_rate = models.IntegerField(default=5)
    tour = models.ForeignKey('Tour',on_delete=models.CASCADE,related_name='rates',null=True)