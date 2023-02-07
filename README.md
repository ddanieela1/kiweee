# Kiwee 

Kiwee is an online photo organizer and photo storage service that allows users to upload and categorize their photos and add new categories as desired. This app was built using django as the framework and Python, its corresponding language. For the styling some bootstrap was added and the rest of the styling was composed of CSS.


## Access the app here:
https://kiweee.herokuapp.com/

## To clone on local machine:

1. Fork and clone this repo into your local machine.
2.Pip install the dependencies psycopg2 and python-dotenv using the command:

```
pip3 install psycopg2 & pip3 install python-dotenv
```

# Wireframe:

![Screen Shot 2023-02-07 at 11 52 45 AM](https://user-images.githubusercontent.com/96893640/217310615-808d4d00-e2bc-4a2e-b025-a52f8e13b26d.png)

# Models:

![Screen Shot 2023-02-07 at 2 40 03 PM](https://user-images.githubusercontent.com/96893640/217348201-b0c1a33b-dde8-4436-97b7-fcbc429cf754.png)

# Sign-in/Register Page:
![Screen Shot 2023-02-07 at 2 43 22 PM](https://user-images.githubusercontent.com/96893640/217348865-e8402453-b7e7-4ecd-bb34-cc755d2ef919.png)

# Homepage:
The side menu shows all categories previously created by the user and will filter search the image with the corresponding category once clicked.

![Screen Shot 2023-02-07 at 2 46 39 PM](https://user-images.githubusercontent.com/96893640/217349519-00ca1fdf-3e61-4fa3-a637-e2669aa031d4.png)

# Photo Upload:
On photo upload users can create a new category or select from a pre-existing category previously created.

![Screen Shot 2023-02-07 at 2 47 02 PM](https://user-images.githubusercontent.com/96893640/217349612-2a47614b-141f-444d-af56-94d9d13d6cb6.png)

# URL's:

```
urlpatterns = [

    path('', views.index, name='index'),
    path('gallery/', views.gallery, name ='gallery'),
    path('main_app/<int:post_id>/', views.viewMedia, name ='viewMedia'),
    path('upload/', views.upload, name ='upload'),

    path('main_app/<int:pk>/delete', views.deletePost.as_view(), name ='post_delete'),
    path('main_app/<int:pk>/update', views.updatePost.as_view(), name ='post_update'),

    path('signup/', views.signup, name ='signup'),
    path('login/', views.login_view, name ='login'),
    path('user/<username>', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('settings/', views.settings, name='settings'),
 
]
```

# Models:
```
class Profile(models.Model):
    name = models.CharField(max_length=50)
    profile_image = models.ImageField('profile_imgs', default= 'media/kiwi-default-pic.jpeg')
    about = models.TextField(max_length= 1000, blank = True)
    location = models.TextField(blank = True, max_length= 100)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    # show name in admin page
    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=100, null = False, blank = False)

    def __str__(self):
        return self.name

class Post(models.Model):
    # unique id for post
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    media = models.ImageField(upload_to='posted_media')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.caption

```

# Routing:

```

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
                return redirect('/gallery/')
              return HttpResponse('Page was found')  
    else:  # it has a get request so send the emtpy login form
        form = AuthenticationForm()
        messages.success(request, ("Error logging in, try again"))
        return render(request, 'login.html', {'form': form})


def signup(request):
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            u = form.cleaned_data['username']
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('/user/'+u)
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


    username= User.objects.get(username=username)
    
    # user = Profile.objects.filter(user=user)
    ctx = {'username':username}
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
```

# Future Improvements:
- Allowing the user to add friends and view others album/photos
- Adding the option of a private photo album
