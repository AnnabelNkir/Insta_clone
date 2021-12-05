from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from insta.models import Image
import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.shortcuts import render, redirect

# Create your views here.

@login_required(login_url='/accounts/login/')
def index(request):
    image = Image.objects.all().order_by('-id')

    return render(request, 'all-photos/index.html',{'image': image})
