from django.shortcuts import render,redirect,get_object_or_404
from django.http  import HttpResponse
import datetime as dt
from .email import send_welcome_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import ImageForm, SignupForm, CommentForm, EditForm
from django.db import models
from .models import Comments, Image,Profile, Likes
from cloudinary.models import CloudinaryField
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Follow

import cloudinary
import cloudinary.uploader
import cloudinary.api

# Create your views here.

from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your Instagram account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can <a href="/accounts/login/">Login</a>  your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def home(request):
    date = dt.date.today()
    
    return render(request, 'registration/homepage.html', {"date": date,})



@login_required(login_url='/home')
def index(request):
    date = dt.date.today()
    photos = Image.objects.all()
    # print(photos)
    profiles = Profile.objects.all()
    # print(profiles)
    form = CommentForm()
    images = Image.get_images().order_by('-posted_on')
    profiles = User.objects.all()
    people = Follow.objects.following(request.user)
    comments = Comments.objects.all()
    likes = Likes.objects.all()

    return render(request, 'all-posts/index.html', {"date": date, "photos":photos, "profiles":profiles, "form":form})

def new_image(request):
    current_user = request.user
    profile = Profile.objects.get(user=current_user)
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = current_user
            image.profile = profile
            image_file = request.FILES['image_file']
            image_file = CloudinaryField.uploader.upload(image_file)
            image.save_image()
        return redirect('index')

    else:
        form = ImageForm()
    return render(request, 'new_image.html', {"form": form})

def profile(request):
    date = dt.date.today()
    current_user = request.user
    profile = Profile.objects.get(user=current_user.id)
    print(profile.profile_pic)
    posts = Image.objects.filter(user=current_user)
    if request.method == 'POST':
        signup_form = EditForm(request.POST, request.FILES,instance=request.user.profile) 
        if signup_form.is_valid():
           signup_form.save()
    else:        
        signup_form =EditForm() 
    
    return render(request, 'registration/profile.html', {"date": date, "form":signup_form,"profile":profile, "posts":posts})

@login_required(login_url='/accounts/login/')
def comment(request,image_id):
    #Getting comment form data
    if request.method == 'POST':
        image = get_object_or_404(Image, pk = image_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.image = image
            comment.save()
    return redirect('index')
    

@login_required(login_url='/accounts/login/')
def search_results(request):
    if 'username' in request.GET and request.GET["username"]:
        search_term = request.GET.get("username")
        searched_users = User.objects.filter(username=search_term)
        message = f"{search_term}"
        profiles=  Profile.objects.all( )
        
        return render(request, 'all-posts/search.html',{"message":message,"users": searched_users,'profiles':profiles})

    else:
        message = "You haven't searched for any term"
        return render(request, 'all-posts/search.html',{"message":message})

def profiles(request,id):
    profile = Profile.objects.get(user_id=id)
    post=Image.objects.filter(user_id=id)
    Comment= Comments.objects.all()
    user = User.objects.get(user_id=id)
    follow = len(Follow.objects.followers(user))
    following = len(Follow.objects.following(user))
    people = Follow.objects.following(request.user)                 
    return render(request,'profiles_each.html',{"profile":profile,"post":post})


@login_required(login_url='/accounts/login/')
def like_image(request):
    image = get_object_or_404(Image, id=request.POST.get('image_id'))
    image.likes.add(request.user)
    return redirect('home')

@login_required(login_url='/accounts/login/')
def follow(request,user_id):
    other_user = User.objects.get(id = user_id)
    follow = Follow.objects.add_follower(request.user, other_user)

    return redirect('home')

@login_required(login_url='/accounts/login/')
def unfollow(request,user_id):
    other_user = User.objects.get(id = user_id)

    follow = Follow.objects.remove_follower(request.user, other_user)

    return redirect('home')
