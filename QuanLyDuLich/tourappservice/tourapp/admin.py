from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class UserAdmin(admin.ModelAdmin):
    search_fields = ('username','first_name','last_name')
    # exclude = ('is_superuser','last_login','password','date_joined')
    readonly_fields = ['avatar_view']
    list_display = ('username','last_name','first_name','last_login','date_joined')
    def avatar_view(self, user):
        return mark_safe(
            "<img src='/static/{url}' alt='test' width='120' />".format(url=user.avatar.name)
        )



admin.site.register(User,UserAdmin)
admin.site.register(Role)
