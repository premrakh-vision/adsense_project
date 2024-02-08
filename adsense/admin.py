from django.contrib import admin
from .models import LiencenceUser , Proxy
# Register your models here.

class LiencenceUserAdmin(admin.ModelAdmin):
    search_fields = ['user', 'key'] 
    readonly_fields  = ('host',) 
    
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