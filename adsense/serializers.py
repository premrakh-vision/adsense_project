from .models import LiencenceUser , UserAgent
from rest_framework import serializers


class LiecenceUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiencenceUser
        fields  = '__all__'

class UserAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAgent
        exclude  = ['is_active']