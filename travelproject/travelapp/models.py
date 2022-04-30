from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    name = models.CharField(max_length = 50, null = False)
    def __str__(self):
        return self.name

class Gender(models.Model):
    gender_type = models.CharField(max_length = 50, null = False)
    def __str__(self):
        return self.gender_type


class User(AbstractUser):
    gender = models.ForeignKey('Gender',related_name='users',null= True,on_delete=models.SET_NULL)
    date_of_birth = models.DateField(null=True)
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


class ImageBase(ModelBase):
    image = models.ImageField(null = True, upload_to = 'images/%Y/%m')
    descriptions = models.CharField(max_length = 255,null = True)
    class Meta:
        abstract = True


class ImageTour(ImageBase):
    tour_info = models.ForeignKey('TourInfo', on_delete = models.CASCADE, related_name = 'images')


class ImageNews(ImageBase):
    news = models.ForeignKey('News', on_delete = models.CASCADE, related_name = 'images')


class News(ModelBase):
    title = models.CharField(max_length = 50, default="none")
    content = models.CharField(max_length = 1024, blank = True)
    author = models.ForeignKey('User', on_delete = models.SET_NULL, related_name = 'list_news', null = True)

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
    description = models.CharField(max_length = 255, blank = True,null = True)
    def __str__(self):
        return self.location


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
    class Meta:
        abstract = True


class Like(ActionBase):
    state = models.BooleanField(default= True)


class CommentNews(CommentBase):
    content = models.CharField(max_length=255,blank= True)


class CommentTour(CommentBase):
    content = models.CharField(max_length=255,blank= True)


class Rate(ActionBase):
    star_rate = models.IntegerField(default=5)