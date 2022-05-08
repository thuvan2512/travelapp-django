from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission,Group
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.template.response import TemplateResponse
from django.utils.safestring import mark_safe
from django import forms
from . import cloud_path
from .models import *
from django.urls import path
from datetime import date

class NewsAdmin(admin.ModelAdmin):
    model = News
    search_fields = ('title',)
    list_display = ('title','author')
    list_filter = ('author','created_date','updated_date')


class TagAdmin(admin.ModelAdmin):
    model = Tag
    search_fields = ('name',)


class MyUserAdmin(UserAdmin):
    model = User
    search_fields = ('username','first_name','last_name')
    list_display = ('username','last_name','first_name','last_login','date_joined')
    list_filter = ()
    readonly_fields = ('last_login','date_joined','avatar_view')
    def avatar_view(self, user):
        if (user.avatar):
            return mark_safe(
                "<img src='{cloud_path}{url}' alt='avatar' width='120' />".format(cloud_path = cloud_path,url=user.avatar)
            )
    fieldsets = (
        ('Login info', {
            'fields': ('avatar_view','avatar','username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'gender','home_town', 'date_of_birth','email','phone')
        }),
        ('Customer', {
            'fields': (
                'is_customer',
            ),
            'description': '<div class="help">%s</div>' % "Designates whether this user is a customer or not",
        }),
        ('Permissions', {
            'fields': (
                'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Other info', {
            'fields': ('is_active','last_login', 'date_joined')
        })
    )


class AttractionsForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Attraction
        fields = '__all__'


class TourForm(forms.ModelForm):
    note = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Tour
        fields = '__all__'


class TourTagInlineAdmin(admin.TabularInline):
    model = Tour.tag.through


class ImageTourInlineAdmin(admin.TabularInline):
    model = ImageTour
    pk_name = 'tour'
    readonly_fields = ('image_view',)
    exclude = ('active',)
    def image_view(self, obj):
        if (obj.image):
            return mark_safe(
                "<img src='{cloud_path}{url}' alt='image-tour' width='120' />".format(cloud_path = cloud_path,url=obj.image)
            )


class TourAdmin(admin.ModelAdmin):
    model = Tour
    exclude = ('tag',)
    list_display = ('name','attraction')
    search_fields = ('name',)
    form = TourForm
    inlines = [TourTagInlineAdmin,ImageTourInlineAdmin]


class AttractionAdmin(admin.ModelAdmin):
    search_fields = ('location',)
    form = AttractionsForm


class ImageTourAdmin(admin.ModelAdmin):
    model = ImageTour
    readonly_fields = ('image_view',)
    search_fields = ('descriptions',)
    def image_view(self, obj):
        if (obj.image):
            return mark_safe(
                "<img src='{cloud_path}{url}' alt='image-tour' width='120' />".format(cloud_path = cloud_path,url=obj.image)
            )
    fieldsets = (
        ('Image of tour', {
            'fields': ('tour','active','image_view','image','descriptions')
        }),
    )


class BookTourAdmin(admin.ModelAdmin):
    list_display = ('name_display','created_date','updated_date')
    def name_display(self,obj):
        return obj.__str__()


class PermissionAdmin(admin.ModelAdmin):
    search_fields = ('name',)


class BillAdmin(admin.ModelAdmin):
    model = Bill
    list_filter = ('payment_state','payment_type','total_price')


class MyAdminSite(admin.AdminSite):
    site_header = 'TRAVEL APP MANAGEMENT'
    site_title = 'Travel App Admin'
    def get_urls(self):
        return [
                   path('stats/', self.stats_view)
               ] + super().get_urls()

    def stats_view(self, request):
        if not request.user.is_superuser:
            raise PermissionDenied
        else:
            data_book_tour = []
            tour_total = Tour.objects.count()
            attraction_total = Attraction.objects.count()
            booking_total = BookTour.objects.filter(created_date__year = date.today().year).count()
            bill_paid_total = Bill.objects.filter(payment_state = True,created_date__year = date.today().year).count()
            results_book_tour = BookTour.objects.filter(created_date__year = date.today().year)\
                .annotate(month=TruncMonth('created_date')).values('month')\
                .annotate(c=Count('pk')).values('month', 'c')
            for i in range(12):
                flag = False
                for rs in results_book_tour:
                    if i + 1 == rs['month'].month:
                        data_book_tour.append(rs['c'])
                        flag = True
                        break
                if not flag:
                    data_book_tour.append(0)
            return TemplateResponse(request, 'admin/stats.html', {
                'tour_total': tour_total,
                'attraction_total':attraction_total,
                'booking_total':booking_total,
                'bill_paid_total':bill_paid_total,
                'current_year': date.today().year,
                'data_book_tour': data_book_tour,
            })



admin_site = MyAdminSite('travelapp')
admin_site.register(User,MyUserAdmin)
admin_site.register(ImageTour,ImageTourAdmin)
admin_site.register(News,NewsAdmin)
admin_site.register(Attraction, AttractionAdmin)
admin_site.register(Tour, TourAdmin)
admin_site.register(Permission,PermissionAdmin)
admin_site.register(Group)
admin_site.register(BookTour,BookTourAdmin)
admin_site.register(Tag,TagAdmin)
admin_site.register(Bill)
admin_site.register(CommentNews)
admin_site.register(CommentTour)
admin_site.register(Rate)

