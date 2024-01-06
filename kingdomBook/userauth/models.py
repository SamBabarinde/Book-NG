from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save


class User(AbstractUser):
    email = models.EmailField(unique=True, null=False)
    username = models.CharField(max_length=75)
    
    USERNAME_FIELD ='email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username
    
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image")
    full_name = models.CharField(max_length=200, null=True, blank=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200) # +234 (456) - 789
    verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.full_name} - {self.bio}"
        
    
def createUserProfile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    
    
def saveUserProfile(sender, instance, **kwargs):
    instance.profile.save()
    
    
post_save.connect(createUserProfile, sender=User)
post_save.connect(saveUserProfile, sender=User)


