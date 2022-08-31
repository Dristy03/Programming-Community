from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


# Creates the profile model.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,primary_key=True,verbose_name="user",related_name='profile',
                                        on_delete=models.CASCADE)
    department = models.CharField(max_length=15,null=True,blank=True)
    batch = models.IntegerField(null=True,blank=True)
    designation = models.CharField(max_length=30, null=True,blank=True)
    reg_num = models.IntegerField(null=True,blank=True)
    mobile_num= models.IntegerField(null=True,blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender,instance,created, **kwargs):
    if created:
        Profile.objects.create(user= instance)

@receiver(post_save, sender=User)
def save_user_profile(sender,instance,**kwargs):
    instance.profile.save()

    
    


