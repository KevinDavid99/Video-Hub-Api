from django.db import models
from cloudinary.models import CloudinaryField
from django.utils import timezone
from django.contrib.auth.models import User
from.validators import validate_file_size
# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name



class Posts(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    image =  CloudinaryField("image", folder='VideoApiPics')
    video = CloudinaryField(resource_type="video", folder='VideoApiVideos', validators=[validate_file_size])
    title = models.CharField(max_length=100, default='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created']

    def __str__(self) -> str:
        if self.title:
            return f"Post by {self.users}, {self.id}: {self.title}"
        else:
            return f'Post {self.id}'
        
    @property 
    def image_url(self): 
        '''This property is used to return or get the image from cloudinary.
        the url is also stored in the database so itl be retrieved like so'''
        return(
            f"https://res.cloudinary.com/dug5dj4uz/image/upload/v{self.image.version}/{self.image}"
        )
    
    @property
    def video_url(self):
        return(
            f'https://res.cloudinary.com/dug5dj4uz/video/upload/v{self.video.version}/{self.video}.mp4'
        )
    
  