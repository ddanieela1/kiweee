from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib import messages


from django.contrib.auth.models import User
from . models import Profile, Post, Category

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout


import cloudinary.uploader



def index(request):
    return render(request, 'main_app/index.html')


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
                    return HttpResponseRedirect('/gallery/')
                else:
                    print('The account has been disabled.')
            else:
                print('The username and/or password is incorrect.')
    else:  # it was a get request so send the emtpy login form
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})


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



def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')



@login_required
def profile(request,username):
    user_object = User.objects.get(username=username)
    user_profile = Profile.objects.get(user=username)
    ctx = {'user_object':user_object, 'user_profile':user_profile}
    return render(request, 'profile.html', ctx)


@login_required
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
def viewMedia(request,post_id):
    post = Post.objects.filter(id=post_id)
    return render(request, 'main_app/show.html', {'post':post})    



@method_decorator(login_required, name='dispatch')
class updatePost(UpdateView):
    model = Post
    fields = ['caption', 'media','category']
    template_name = 'main_app/post_update.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect('/main_app/' + str(self.object.id))




@method_decorator(login_required, name='dispatch')
class deletePost(DeleteView):
    model = Post
    success_url = reverse_lazy('gallery')


@login_required
def upload(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        upload_data = request.POST
        media = request.FILES.get('media')

        if upload_data['category'] != None:
            category = Category.objects.get(id=upload_data['category'])
        elif upload_data['category'] != '':
            category = Category.objects.get_or_create(name =upload_data['category'])
        else:
            category = None

        post = Post.objects.create(
            user = request.user,
            category = category,
            caption = upload_data['caption'],
            media = media
        )
        post.save()
        return redirect('gallery')
    
    return render(request, 'main_app/upload.html', {'categories':categories})


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
