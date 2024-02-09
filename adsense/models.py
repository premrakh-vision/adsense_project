from django.db import models
import uuid
import secrets
import string
from django.core.mail import send_mail
from ad_project import settings
# Create your models here.


class LiencenceUser(models.Model):
    user = models.CharField(max_length=100 , unique=True)
    email = models.EmailField(unique=True)
    key = models.CharField(max_length= 50 , unique=True,null=True,blank=True)
    host = models.CharField(max_length=100,unique=True, null=True , blank=True) 
    valid_end_date = models.DateTimeField()
    
    def __str__(self): 
        return f"{self.host}-{self.user}"
    
    def save(self, *args, **kwargs):
        if not self.key:  # Generate a key only if it doesn't exist already
            self.key = uuid.uuid4()
            super(LiencenceUser, self).save(*args, **kwargs)
        else:
            super(LiencenceUser, self).save(*args, **kwargs)
 
 
class Proxy(models.Model):
    user = models.ManyToManyField(LiencenceUser , related_name = 'proxy')
    proxy = models.CharField(max_length = 255,unique = True)

    def __str__(self) -> str:
        return self.proxy
