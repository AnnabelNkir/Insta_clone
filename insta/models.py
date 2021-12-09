from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    first_name = models.CharField(max_length=30,default="Some String")
    last_name = models.CharField(max_length=30,default="Some String")
    bio = models.CharField(max_length=200)
    profile_pic = models.ImageField(upload_to='profile/')
    pub_date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.first_name

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def get_profiles(cls):
        profiles = cls.objects.all()
        return profiles
    
    @classmethod
    def search_by_username(cls,search_term):
        profiles = cls.objects.filter(title__icontains=search_term)
        return profiles
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Image(models.Model):
    image = models.ImageField(upload_to = 'images/', blank=True)
    image_name = models.CharField(max_length=30,default="Some String")
    image_caption = models.CharField(max_length = 300)
    image_location = models.CharField(max_length=30,null=True)
    likes= models.ManyToManyField(User,default=None,blank=True,related_name='liked')
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True)
    post_date = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering =('-post_date',)

    def save_images(self):
        self.save()
    
    def del_img(self):
                self.delete()
    
    @classmethod
    def get_images(cls):
        images = Image.objects.all()
        return images
    
    @property
    def count_likes(self):
                likes = self.likes.count()
                return likes

class Comments(models.Model):
    comment = models.CharField(max_length = 300)
    posted_on = models.DateTimeField(auto_now=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save_comment(self):
        self.save()

    def delete_comment(self):
        self.delete()

    @classmethod
    def get_comments_by_images(cls, id):
        comments = Comments.objects.filter(image__pk = id)
        return comments

class Likes(models.Model):
        user_like = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
        liked_post =models.ForeignKey(Image, on_delete=models.CASCADE, related_name='likes')

        def save_like(self):
                self.save()

        def __str__(self):
                return self.user_like


