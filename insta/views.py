from django.shortcuts import render
from .models import Images,Profile,Likes,Comments
from django.contrib.auth.decorators import login_required
import cloudinary
import cloudinary.uploader
import cloudinary.api



# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):
    image = Images.objects.all().order_by('-id')
    return render(request, 'instapp/index.html',{'image':image})
