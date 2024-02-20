from django.db import models
import uuid
import secrets, pytz
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
            self.proxy.set(Proxy.objects.all())
        else:
            super(LiencenceUser, self).save(*args, **kwargs)
 
 
class Proxy(models.Model):

    # Get the common timezones
    common_timezones = pytz.common_timezones

    # Transform the list of timezone strings into a list of tuples
    TIMEZONE_CHOICES = [(tz, tz) for tz in common_timezones]

    user = models.ManyToManyField(LiencenceUser , related_name = 'proxy')
    proxy = models.CharField(max_length = 255,unique = True)
    timezone = models.CharField(max_length = 500, choices=TIMEZONE_CHOICES, null=True)

    def __str__(self) -> str:
        return self.proxy
