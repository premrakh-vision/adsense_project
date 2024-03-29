from django.db import models
import uuid
import pytz
import os
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class LiencenceUser(models.Model):
    user = models.CharField(max_length=100 , unique=True)
    email = models.EmailField(unique=True)
    key = models.CharField(max_length= 50 , unique=True,null=True,blank=True)
    host = models.CharField(max_length=100,unique=True, null=True , blank=True) 
    valid_end_date = models.DateTimeField()
    is_static_proxy = models.BooleanField(default=False)
    
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
    timezone = models.CharField(max_length = 500, choices=TIMEZONE_CHOICES, default = 'US/Central')

    def __str__(self) -> str:
        return self.proxy


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            # If the file with the same name exists, remove it before saving the new one
            os.remove(os.path.join(self.location, name))
        return name

class StaticFile(models.Model):
    file_name = models.CharField(max_length=100,choices = (('static_proxy','static_proxy'),('user_agent','user_agent')) ,null=True, blank=True)
    file = models.FileField(upload_to='static/adsense_exe_files/', storage=OverwriteStorage())

    def save(self, *args, **kwargs):
        if self.file_name:
            extension = self.file.name.split('.')[-1]  # Get the file extension
            new_file_name = f"{self.file_name}.{extension}"
            self.file.name = new_file_name
        super(StaticFile, self).save(*args, **kwargs)
    
    def __str__(self):
        
        if self.file_name:
            return self.file_name
        else:
            return self.file.name

       
class UserAgent(models.Model):
    platform = models.CharField(max_length = 500 , unique = True)
    os_min_version = models.IntegerField(default = 10) 
    os_max_version = models.IntegerField(default = 15)
    browser_string = models.CharField(default = "Version/{version}.0 Mobile Safari/537.36")
    device_list = ArrayField(models.CharField(), blank=True , default=list)
    is_active = models.BooleanField(default = True)
    browser_versions = ArrayField(models.CharField(), blank=True , default=list)
    apple_webkit_versions = ArrayField(models.CharField(), blank=True , default=list)
    
    def __str__(self) -> str:
        return self.platform
    