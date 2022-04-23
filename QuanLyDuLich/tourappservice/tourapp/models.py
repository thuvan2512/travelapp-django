from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    name = models.CharField(max_length = 50, null = False)
    def __str__(self):
        return self.name


class User(AbstractUser):
    date_of_birth = models.DateTimeField(null=True)
    avatar = models.ImageField(null=True, upload_to='users/%Y/%m')
    role = models.ForeignKey('Role', related_name='users',null = True,on_delete = models.SET_NULL)
    home_town = models.CharField(max_length=50,null= True, blank= True)
    phone = models.CharField(max_length=10,null= True, blank= True)


class ModelBase(models.Model):
    active = models.BooleanField(default = True)
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)
    class Meta:
        abstract = True


class Image(ModelBase):
    image = models.ImageField(null = True, upload_to = 'images/%Y/%m')
    descriptions = models.CharField(max_length = 255,null = True)
    class Meta:
        abstract = True


class ImageTour(Image):
    tour = models.ForeignKey('Tour', on_delete = models.CASCADE, related_name = 'images')


class ImageNews(Image):
    news = models.ForeignKey('News', on_delete = models.CASCADE, related_name = 'images')


class News(ModelBase):
    title = models.CharField(max_length = 50, default="none")
    content = models.CharField(max_length = 1024, blank = True)
    author = models.ForeignKey('User', on_delete = models.SET_NULL, related_name = 'list_news', null = True)


class Tour(ModelBase):
    price_for_adults = models.FloatField(default = 0)
    price_for_children = models.FloatField(default = 0)
    location = models.CharField(max_length = 50, default="none")
    departure_date = models.DateTimeField(null = True)
    end_date = models.DateTimeField(null=True)
    description = models.CharField(max_length = 255, blank = True,null = True)
    customer = models.ManyToManyField('User', through= 'BookTour')


class BookTour(ModelBase):
    user = models.ForeignKey('User',on_delete=models.CASCADE)
    tour = models.ForeignKey('Tour',on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    num_of_adults = models.IntegerField(default=0)
    num_of_children = models.IntegerField(default=0)