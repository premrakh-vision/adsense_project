"""
URL configuration for ad_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path ,  include , re_path 
from rest_framework.routers import DefaultRouter
from adsense.views import LiencenceUserView , ProxyView, ProxyTimezoneView , populate_proxies , edit_timezone , UserAgentView
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve 
router = DefaultRouter()

router.register('user', LiencenceUserView , basename='user')
router.register('proxy', ProxyView , basename='proxy')
router.register('proxy_timezone', ProxyTimezoneView , basename='proxy_timezone')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('licence/',include(router.urls)),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('populate-proxies/', populate_proxies, name='populate_proxies'),
    path('edit_timezone/', edit_timezone, name='edit_timezone'),
    path('user_agent/', UserAgentView.as_view({'get': 'custom_action'}), name='custom_action'),
]

