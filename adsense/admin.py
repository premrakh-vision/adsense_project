from .models import StaticFile
from django.contrib import admin
from .models import LiencenceUser, Proxy, UserAgent, AdsenseLog
from django.contrib.admin.helpers import ActionForm
from django import forms

from .forms import StaticFileForm

# Register your models here.


class LiencenceUserForm(ActionForm):
    is_static_proxy = forms.BooleanField(required=False, label="Static Proxy")


class LiencenceUserAdmin(admin.ModelAdmin):
    search_fields = ["user", "key", "host"]
    readonly_fields = ("host",)
    list_display = ("host", "user", "key", "valid_end_date", "is_static_proxy")
    actions = ["change_user_detail"]
    action_form = LiencenceUserForm

    def change_user_detail(self, request, queryset):
        if request.POST.get("is_static_proxy"):
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
    filter_horizontal = ("user",)


class StaticFileAdmin(admin.ModelAdmin):
    form = StaticFileForm


class UseragentForm(ActionForm):
    is_active = forms.BooleanField(required=False, label="Active")


class UseragentAdmin(admin.ModelAdmin):
    list_display = ("platform", "is_active")
    actions = ["change_useragent_activity"]
    action_form = UseragentForm

    def change_useragent_activity(self, request, queryset):
        if request.POST.get("is_active"):
            queryset.update(is_active=True)
        else:
            queryset.update(is_active=False)

    change_useragent_activity.short_description = "Change Useragent activity"

class AdsenseLogAdmin(admin.ModelAdmin):
    list_display = ["user", "website", "ip", "host", "key", "created_at"]


admin.site.register(StaticFile, StaticFileAdmin)
# Register the model with the custom admin class
admin.site.register(LiencenceUser, LiencenceUserAdmin)
admin.site.register(Proxy, ProxyModelAdmin)

admin.site.register(UserAgent, UseragentAdmin)

admin.site.register(AdsenseLog, AdsenseLogAdmin)
