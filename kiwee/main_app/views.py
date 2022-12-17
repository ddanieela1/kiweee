from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.exceptions import ValidationError
import uuid

from django.contrib.auth.models import User
from . models import Profile, Post, Category

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


import cloudinary.uploader
# Create your views here.


def index(request):
    return render(request, 'main_app/index.html')


def gallery(request):
    category = request.GET.get('category')

    if category == None:
        posts = Post.objects.all()
    else:
        posts = Post.objects.filter(category__name = category)

    categories = Category.objects.all()
    ctx = {'categories': categories, 'posts': posts}
    return render(request, 'gallery.html', ctx)



@login_required
def homepage(request):
    user_object = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user = user_object)
    return render(request, 'profile.html', {'profile': profile})
   


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username=u, password=p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/user/'+u)
                else:
                    print('The account has been disabled.')
            else:
                print('The username and/or password is incorrect.')
    else:  # it was a get request so send the emtpy login form
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})



def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            u = form.cleaned_data['username']
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('/user/'+u)

        elif request.POST['username'] == request.POST['username'].exists():
            username = form.cleaned_data['username']
            messages.info(request, 'Username already in use.')
            return redirect('/signup')

        else:
            return render(request, 'signup.html', {'form': form})

    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})



@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    return render(request, 'profile.html', {'username': username})



def viewMedia(request,pk):
    post = Post.objects.get(pk=id)
    return render(request, 'show.html', {'post':post})    


def upload(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        upload_data = request.POST
        media = request.FILES.get('media')

        if upload_data['category'] != 'none':
            category = Category.objects.get(id=upload_data['category'])
        elif upload_data('category_net') != '':
            category, created = Category.objects.get_or_create(name =upload_data['category_new'])
        else:
            category = None    

        post = Post.objects.create(
            category = category,
            caption = upload_data['caption'],
            media = media
        )    
        ctx = {'categories': categories}
        return render(request, 'main_app/upload.html', ctx)

    return redirect('gallery')



@login_required
def settings(request):

    user_profile = Profile.objects.filter(user=request.user)
    if request.method == 'POST':
        try:
            if request.FILES.get('image') != None:
                image = request.FILES.get('profile_image')
                about = request.POST['about']
                location = request.POST['location']

                user_profile.profile_image = image
                user_profile.about = about
                user_profile.location = location
                user_profile.save()

            if request.FILES.get('image') == None:
                image = user_profile.profile_image
                about = request.POST['about']
                location = request.POST['location']

                user_profile.profile_image = image
                user_profile.about = about
                user_profile.location = location
                user_profile.save()

        except Profile.DoesNotExist:
            user_profile = None

        return redirect('settings')

    return render(request, 'settings.html', {'user_profile': user_profile})
