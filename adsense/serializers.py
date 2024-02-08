from .models import LiencenceUser
from rest_framework import serializers


class LiecenceUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiencenceUser
        fields  = '__all__'
