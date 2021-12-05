from django.db import models
from cloudinary.models import CloudinaryField
import datetime as dt
from django.contrib.auth.models import User
from django.db.models.fields import related

# Create your models here.
class Image(models.Model):
    # title field
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image')
    title = models.CharField(max_length=50)
    caption = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True,null=True)
    profile = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title

    def save_images(self):
        self.save()

        # delete image
    def delete_image(self):
        self.delete()

    @classmethod
    def get_images_by_user(cls, user):
        images = cls.objects.filter(user=user)
        return images


    def update_images(self, title, caption):
        self.title = title
        self.caption = caption
        self.save()

    # get all images
    @classmethod
    def get_all_images(cls):
        today = dt.date.today()
        images = Image.objects.all(post_date__date = today)
        return images
    
    class Profile(models.Model):
     prof_photo = CloudinaryField('image')
    bio = models.TextField(max_length=1000, blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.phone_number

    def save_profile(self):
        self.save()

    def update_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def get_profile_by_user(cls, user):
        profile = cls.objects.filter(user=user)
        return 