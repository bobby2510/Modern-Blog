from django.contrib.auth.models import User
from django.db import models



class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(default='default.jpg',upload_to='profile_images')
    country=models.CharField(null=True,blank=True,max_length=20)
    state=models.CharField(null=True,blank=True,max_length=20)
    city=models.CharField(null=True,blank=True,max_length=20)
    about_me=models.CharField(null=True,blank=True,max_length=100)    

    def __str__(self):
        return f'{self.user.username} -profile'