from django.contrib import admin
from .models import Images,Profile,Comments,Likes

# Register your models here.
admin.site.register(Images)
admin.site.register(Likes)
admin.site.register(Profile)
admin.site.register(Comments)