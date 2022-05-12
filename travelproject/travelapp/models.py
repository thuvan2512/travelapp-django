from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import  CloudinaryField
from ckeditor.fields import RichTextField



class Gender(models.Model):
    gender_type = models.CharField(max_length = 50, null = False)
    def __str__(self):
        return self.gender_type


class User(AbstractUser):
    email = models.EmailField(unique=True,null=True)
    gender = models.ForeignKey('Gender',related_name='users',null= True,on_delete=models.SET_NULL)
    date_of_birth = models.DateField(null=True)
    avatar = CloudinaryField('avatar',default = '', null = True)
    is_customer = models.BooleanField(default= False,verbose_name='Customer status')
    home_town = models.CharField(max_length=50,null= True, blank= True)
    phone = models.CharField(max_length=10,null= True, blank= True)
    def __str__(self):
        return self.username


class ModelBase(models.Model):
    active = models.BooleanField(default = True)
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)
    class Meta:
        abstract = True


class ImageTour(ModelBase):
    image = CloudinaryField('image',default = '')
    descriptions = models.CharField(max_length = 255,null = True)
    tour = models.ForeignKey('Tour', on_delete = models.CASCADE, related_name = 'images',null=True)
    class Meta:
        verbose_name = 'Image of tour'
    def __str__(self):
        return self.descriptions



class News(ModelBase):
    title = models.CharField(max_length = 255, default="none")
    content = RichTextField(null=True)
    author = models.ForeignKey('User', on_delete = models.SET_NULL, related_name = 'list_news', null = True)
    class Meta:
        verbose_name = 'New'
    def __str__(self):
        return self.title

class Tour(ModelBase):
    name = models.CharField(max_length=100,null= False, default="none")
    price_for_adults = models.FloatField(default = 0)
    price_for_children = models.FloatField(default = 0)
    departure_date = models.DateField(null = True)
    end_date = models.DateField(null=True)
    attraction = models.ForeignKey('Attraction',on_delete=models.PROTECT,related_name='tours',null=True)
    customers = models.ManyToManyField('User', through= 'BookTour',related_name='tours')
    note = RichTextField(null=True)
    tag = models.ManyToManyField('Tag',related_name='tours')
    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name


class Attraction(ModelBase):
    location = models.CharField(max_length = 50, default="none")
    description = RichTextField(null=True)
    def __str__(self):
        return self.location


class BookTour(ModelBase):
    user = models.ForeignKey('User',on_delete=models.CASCADE)
    tour = models.ForeignKey('Tour',on_delete=models.CASCADE)
    num_of_adults = models.IntegerField(default=0)
    num_of_children = models.IntegerField(default=0)
    send_mail = models.BooleanField(default=False)
    def __str__(self):
        return " \"{0}\" --- \"{1}\" ".format(self.user.__str__(),self.tour.__str__())
    class Meta:
        unique_together = ('user', 'tour')


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
    state = models.BooleanField(default= False )
    news = models.ForeignKey('News', on_delete=models.CASCADE, related_name='likes',null= True)
    class Meta:
        unique_together = ('user', 'news')


class CommentNews(CommentBase):
    news = models.ForeignKey('News',on_delete=models.CASCADE,related_name='comments',null= True)
    def __str__(self):
        return " \"{0}\" --- \"{1}\" ".format(self.user.__str__(),self.news.__str__())


class CommentTour(CommentBase):
    tour = models.ForeignKey('Tour',on_delete=models.CASCADE,related_name='comments',null= True)
    def __str__(self):
        return " \"{0}\" --- \"{1}\" ".format(self.user.__str__(),self.tour.__str__())


class Rate(ActionBase):
    star_rate = models.IntegerField(default=5)
    tour = models.ForeignKey('Tour',on_delete=models.CASCADE,related_name='rate',null=True)
    def __str__(self):
        return " \"{0}\" --- \"{1}\" ".format(self.user.__str__(),self.tour.__str__())
    class Meta:
        unique_together = ('user', 'tour')

class TypeOfPayment(models.Model):
    payment_type = models.CharField(max_length=50, null=False)
    def __str__(self):
        return self.payment_type

class Bill(ModelBase):
    book_tour = models.OneToOneField('BookTour',on_delete=models.CASCADE,primary_key=True)
    payment_state = models.BooleanField(default= False)
    payment_type = models.ForeignKey('TypeOfPayment', on_delete= models.PROTECT,related_name='bills',null=True,default=None)
    total_price = models.FloatField(default=0)
    def __str__(self):
        return "Bill --- {}".format(self.book_tour.__str__())


class CodeConfirm(models.Model):
    user = models.OneToOneField('User',on_delete=models.CASCADE,primary_key=True)
    code = models.CharField(max_length=100)


class NewsView(models.Model):
    news = models.OneToOneField('News',on_delete= models.CASCADE,primary_key=True)
    views = models.IntegerField(default=0)
    updated_date = models.DateTimeField(auto_now=True)