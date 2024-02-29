from django.contrib import admin
from .models import LiencenceUser , Proxy
from django.contrib.admin.helpers import ActionForm
from django import forms

# Register your models here.

class LiencenceUserForm(ActionForm):
    is_static_proxy = forms.BooleanField(required=False,label = 'Static Proxy')

class LiencenceUserAdmin(admin.ModelAdmin):
    search_fields = ['user', 'key'] 
    readonly_fields  = ('host',) 
    list_display = ('host', 'user', 'key', 'valid_end_date' , 'is_static_proxy')
    actions = ['change_user_detail']
    action_form = LiencenceUserForm
    
    def change_user_detail(self, request, queryset):
        if request.POST.get('is_static_proxy'):
            queryset.update(is_static_proxy=True) 
        else:
            queryset.update(is_static_proxy=False) 

    change_user_detail.short_description = "Change User Detail"
    
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False
    
    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False
 
    
class ProxyModelAdmin(admin.ModelAdmin):
    filter_horizontal = ('user',)

# Register the model with the custom admin class
admin.site.register(LiencenceUser, LiencenceUserAdmin)
admin.site.register(Proxy,ProxyModelAdmin)