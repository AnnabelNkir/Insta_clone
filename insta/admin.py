from django.contrib import admin
from .models import Image,Profile,Like,Comment,Follows
# Register your models here.
admin.site.register(Image)
admin.site.register(Profile)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Follows)


