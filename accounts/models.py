from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

def user_directory_path(instance, filename):
    return f'user_{instance.user.id}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to=user_directory_path,blank=True, null=True)


    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User) 
def create_or_update_user_profile(sender, instance, created,  **kwargs ):
    
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()      