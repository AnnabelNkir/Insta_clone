from django.db import models
from cloudinary.models import CloudinaryField
from django.db.models.fields import related
from django.contrib.auth.models import User


# Create your models here
class Images(models.Model):
    image = CloudinaryField('image')
    name = models.CharField(max_length=50)
    caption = models.TextField(max_length=2000)
    pub_date = models.DateTimeField(auto_now_add=True,null=True)
    likes_count = models.IntegerField(default=0)
    comm_count = models.IntegerField(default=0)
    profile = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='image',null=True)
    def __str__(self):
        return self.name

    def update_caption(self, new_caption):
        self.image_caption = new_caption
        self.save()

    @classmethod
    def get_images_by_user(cls, user):
        images = cls.objects.filter(user=user)
        return images

    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()

    @classmethod
    def search_by_image_name(cls, search_term):
        images = cls.objects.filter(
            image_name__icontains=search_term)
        return images
    