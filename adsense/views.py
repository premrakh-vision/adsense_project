from django.shortcuts import render
from rest_framework import viewsets
from .models import LiencenceUser , Proxy , UserAgent 
from .serializers import LiecenceUserSerializer , AdsenseLogSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .utils import device_resolutions
# Create your views here.

class LiencenceUserView(viewsets.ViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def list(self,request):
        try:
            host = request.query_params.get('host')
            key = request.query_params.get('key')
            user = LiencenceUser.objects.get(host=host , key=key)
            if user:
                d1 = LiecenceUserSerializer(user )
                return Response(d1.data , status=status.HTTP_200_OK)
            return Response({'error':'Invalid Crediential'} ,  status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({'error':str(e)} , status=status.HTTP_400_BAD_REQUEST)
        
    def partial_update(self, request,pk=None):
        try:
            key = request.data['key']
            host= request.data['host']
            user = LiencenceUser.objects.get(key = key)
            if user.host == None:
                d1 = LiecenceUserSerializer(user,data=request.data, partial=True)
                if d1.is_valid():
                    d1.save()
                    return Response(d1.data,status=status.HTTP_200_OK)
                return Response(d1.errors,status=status.HTTP_400_BAD_REQUEST)
            return Response({'error':'User Already Updated'},status=status.HTTP_304_NOT_MODIFIED)
        except:
            return Response({'error':'Invalid Key'},status=status.HTTP_400_BAD_REQUEST)
        
    
class ProxyView(viewsets.ViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def list(self,request):
        try:
            host = request.query_params.get('host')
            user = LiencenceUser.objects.get(host = host)
            proxy_query_data = user.proxy.all()
            list_of_proxy = []
            for proxy in proxy_query_data:
                list_of_proxy.append(proxy.proxy)
            return Response(list_of_proxy,status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error':{str(e)}} , status=status.HTTP_404_NOT_FOUND)


class ProxyTimezoneView(viewsets.ViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def list(self,request):
        try:
            host = request.query_params.get('host')
            user = LiencenceUser.objects.get(host = host)
            proxy_query_data = user.proxy.all()
            list_of_proxy = []
            for proxy_obj in proxy_query_data:
                list_proxy = [item.strip() for item in proxy_obj.proxy.split('\n') if item.strip()]
                for proxy in list_proxy:
                    list_of_proxy.append({
                        'proxy': proxy,
                        'timezone': proxy_obj.timezone
                        })
            return Response(list_of_proxy,status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error':{str(e)}} , status=status.HTTP_404_NOT_FOUND)


class UserAgentView(viewsets.ViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def custom_action(self,request):
        user_agent_data = UserAgent.objects.filter(is_active=True)

        browsers = dict(user_agent_data.values_list('platform' , 'browser_string'))
        platforms = list(browsers.keys())
        devices = dict(user_agent_data.values_list('platform' , 'device_list'))
        browser_versions = dict(user_agent_data.values_list('platform' , 'browser_versions'))
        apple_webkit_versions = dict(user_agent_data.values_list('platform' , 'apple_webkit_versions'))
        os_versions = {}

        for user_agent in user_agent_data:
            platform = user_agent.platform
            version_list  = [str(version) for version in range(user_agent.os_min_version , user_agent.os_max_version)]
            os_versions[platform] = version_list

        all_data = {
            "platforms" : platforms,
            "os_versions": os_versions,
            "browsers": browsers,
            "devices": devices,
            "browser_versions": browser_versions,
            "apple_webkit_versions": apple_webkit_versions,
            "device_resolutions": device_resolutions
        }
        
        print(all_data)
        return Response(all_data,status=status.HTTP_200_OK)
  
class AdsenseLogView(viewsets.ViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def create(self,request):
        try:
            data = request.data
            serialize_data = AdsenseLogSerializer(data=data)
            if serialize_data.is_valid(raise_exception=True):
                serialize_data.save()
                return Response({"Success" : True} , status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Success" : False} , status=status.HTTP_400_BAD_REQUEST)


import pytz
from django.http import JsonResponse
from django.db import transaction

def populate_proxies(request):
    try:
        with open('proxy.txt', 'r') as file:
            proxies = [proxy.strip() for proxy in file]

        # Create Proxy instances
        proxy_instances = [Proxy(proxy=proxy) for proxy in proxies]

        # Bulk create Proxy instances
        Proxy.objects.bulk_create(proxy_instances)

        # Retrieve all users once
        users = list(LiencenceUser.objects.all())
        a = 1
        with transaction.atomic():
            for proxy_instance in Proxy.objects.all():
                proxy_instance.user.add(*users)
                print(a)
                a+=1

    except Exception as e:
        return JsonResponse({'message': 'Error occurred: {}'.format(str(e))}, status=500)

    return JsonResponse({'message': 'Successfully added proxies and associated users'})
    
    # print('********')
    # Proxy.objects.all().delete()

    # return JsonResponse({'message': 'Successfully deleted proxies and associated users'})
 
common_timezones = pytz.common_timezones
import random
# Transform the list of timezone strings into a list of tuples
TIMEZONE_CHOICES = [(tz, tz) for tz in common_timezones]

def edit_timezone(request):
    proxy_list = Proxy.objects.all()
    for proxy in proxy_list:
        proxy.timezone = 'US/Central'
        proxy.save()
    return JsonResponse({'message': 'Successfully added proxies and associated users'})