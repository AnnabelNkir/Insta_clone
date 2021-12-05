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
    return render(request, 'all-photos/index.html',{'image':image})

@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user
    pics = Images.objects.filter(user_id=current_user.id)
    profile = Profile.objects.filter(user_id=current_user.id).first()
    return render(request, 'all-photos/index.html', {"pics": pics, "profile": profile})

@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user
    pics = Images.objects.filter(user_id=current_user.id)
    profile = Profile.objects.filter(user_id=current_user.id).first()
    return render(request, 'profile.html', {"pics": pics, "profile": profile})