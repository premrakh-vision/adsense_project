from .models import StaticFile
from django.contrib import admin
from .models import LiencenceUser , Proxy
from .forms import StaticFileForm
# Register your models here.

class LiencenceUserAdmin(admin.ModelAdmin):
    search_fields = ['user', 'key'] 
    readonly_fields  = ('host',) 
    list_display = ('host', 'user', 'key', 'valid_end_date')
    
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


class StaticFileAdmin(admin.ModelAdmin):
    form = StaticFileForm

admin.site.register(StaticFile, StaticFileAdmin)
# Register the model with the custom admin class
admin.site.register(LiencenceUser, LiencenceUserAdmin)
admin.site.register(Proxy,ProxyModelAdmin)