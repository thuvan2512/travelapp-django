from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Count, Sum
from django.template.response import TemplateResponse
from django.utils.safestring import mark_safe
from django import forms
from .models import *
from django.urls import path


class NewsAdmin(admin.ModelAdmin):
    # model = News
    search_fields = ('title',)
    list_display = ('title','author')
    list_filter = ('author','created_date','updated_date')

class MyUserAdmin(UserAdmin):
    model = User
    search_fields = ('username','first_name','last_name')
    list_display = ('username','last_name','first_name','last_login','date_joined')
    list_filter = ()
    readonly_fields = ('last_login','date_joined','avatar_view')
    def avatar_view(self, user):
        if (user.avatar):
            return mark_safe(
                "<img src='https://res.cloudinary.com/dec25/{url}' alt='avatar' width='120' />".format(url=user.avatar)
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
                "<img src='https://res.cloudinary.com/dec25/{url}' alt='image-tour' width='120' />".format(url=obj.image)
            )


class TourAdmin(admin.ModelAdmin):
    exclude = ('tag',)
    form = TourForm
    inlines = [TourTagInlineAdmin,ImageTourInlineAdmin]


class TourInfoAdmin(admin.ModelAdmin):
    form = AttractionsForm

class ImageTourAdmin(admin.ModelAdmin):
    model = ImageTour
    readonly_fields = ('image_view',)
    def image_view(self, obj):
        if (obj.image):
            return mark_safe(
                "<img src='https://res.cloudinary.com/dec25/{url}' alt='image-tour' width='120' />".format(url=obj.image)
            )
    fieldsets = (
        ('Image of tour', {
            'fields': ('tour','active','image_view','image','descriptions')
        }),
    )

class MyAdminSite(admin.AdminSite):
    site_header = 'TRAVEL APP MANAGEMENT'
    site_title = 'Travel App Admin'
    def get_urls(self):
        return [
                   path('tours-stats/', self.stats_view)
               ] + super().get_urls()
    def stats_view(self, request):
        labels =[]
        data = []
        count = Tour.objects.count()
        booking_stats = Tour.objects.annotate(booking_counter=Count('customers')).values('id', 'name', 'booking_counter').order_by('-booking_counter')
        booking_total = BookTour.objects.count()
        for s in booking_stats:
            labels.append(s['name'])
            data.append(s['booking_counter'])
        return TemplateResponse(request, 'admin/tours-stats.html', {
            'count': count,
            'booking_stats': booking_stats,
            'booking_total':booking_total,
            'labels': labels,
            'data': data,
        })



admin_site = MyAdminSite('travelapp')
admin_site.register(User,MyUserAdmin)
admin_site.register(ImageTour,ImageTourAdmin)
admin_site.register(News,NewsAdmin)
admin_site.register(Attraction, TourInfoAdmin)
admin_site.register(Tour, TourAdmin)
admin_site.register(BookTour)
admin_site.register(Tag)
admin_site.register(Bill)
