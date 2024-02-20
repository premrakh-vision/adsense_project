from django.shortcuts import render
from rest_framework import viewsets
from .models import LiencenceUser , Proxy
from .serializers import LiecenceUserSerializer 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
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
            for proxy in proxy_query_data:
                list_of_proxy.append({
                    'proxy': proxy.proxy,
                    'timezone': proxy.timezone
                    })
            return Response(list_of_proxy,status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error':{str(e)}} , status=status.HTTP_404_NOT_FOUND)