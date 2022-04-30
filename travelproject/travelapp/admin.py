from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from django import forms
from .models import *


# class UserAdmin(admin.ModelAdmin):
#     search_fields = ('username','first_name','last_name')
#     exclude = ('is_superuser','last_login','password','date_joined')
#     readonly_fields = ['avatar_view']
#     list_display = ('username','last_name','first_name','last_login','date_joined')
#     def avatar_view(self, user):
#         return mark_safe(
#             "<img src='/static/{url}' alt='test' width='120' />".format(url=user.avatar.name)
#         )

# class BookTourAdmin(admin.ModelAdmin):


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
        ('Permissions', {
            'fields': (
                'is_staff', 'is_superuser','is_customer',
                'groups', 'user_permissions'
                )
        }),
        ('Other info', {
            'fields': ('is_active','last_login', 'date_joined')
        })
    )

class TourInfoForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = TourInfo
        fields = '__all__'

class TourInfoAdmin(admin.ModelAdmin):
    form = TourInfoForm


admin.site.register(User,MyUserAdmin)
admin.site.register(ImageTour)
admin.site.register(News)
admin.site.register(TourInfo,TourInfoAdmin)
admin.site.register(Tour)
admin.site.register(BookTour)
