from django.contrib import admin
from .models import Comments, Likes, Profile,Image

# Register your models here.

admin.site.register(Profile)
admin.site.register(Image)
admin.site.register(Comments)
admin.site.register(Likes)
