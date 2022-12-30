# def signup_view(request):
#     if request.method == 'POST':
#         username = request.POST.get['username']
#         email = request.POST.get['email']
#         password = request.POST.get['password']
#         password2 = request.POST.get['password2']

#         if password == password2:
#             if User.objects.filter(username=username).exists():
#                 messages.info(request, 'Username already in use.')
#                 return redirect('/signup')
#             elif User.objects.filter(email=email).exists():
#                 messages.info(request, 'Email is already registered.')  
#                 return redirect('/signup')  
#             else:
#                 newuser = User.objects.create_user(username=username, email=email, password=password)
#                 newuser.save()
#                 return redirect('/profile')
#         else:
#             messages.info(request,'Passwords dont match')    
#     else:
#         return render(request, 'signup.html')




    # <input type="text" name="username" placeholder="Username" >
    # <input type="email" name="email" placeholder="e-mail" >
    # <input type="password" name="password" placeholder="Password" >
    # <input type="password" name="password2" placeholder="Confirm Password" >
    # <button type="submit">Sign up</button>


    @login_required
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        media = request.FILES.get('media_upload')
        caption = request.POST.get['caption']

        uploaded_post = Post.objects.create(user=user, media=media, caption=caption)
        uploaded_post.save()
        return redirect('/homepage')
    else:
        return redirect('/profile')








                        <!-- </div>
                        <a href="{% url 'updatePost' media.id %}">Update</a>
                        </div>

                            <div>
                                <a href = "{% url 'deletePost' media.id %}">Delete</a>
                            </div> -->


            <!-- <a href="{% url 'updatePost' post.id %}" class="btn btn-warning">Update Details</a> -->



                    <a href="/main_app/{{post.id}}/delete" class="btn btn-danger">Delete This Post</a>

            <a href="{% url 'post_delete' post.id %}" class="btn btn-danger">Delete This Post</a>





# @method_decorator(login_required, name='dispatch')
# class updatePost(UpdateView):
#     model = Post
#     fields = ['caption', 'media','category']
    

#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.save()
#         return HttpResponseRedirect('/gallery/' + str(self.object.id))    


@method_decorator(login_required, name='dispatch')
class updatePost(UpdateView):
    model = Post
    fields = ['caption', 'media','category']
    template_name = 'main_app/post_update.html'

    

    def form_valid(self):
        pk = self.kwargs['pk']
        return reverse_lazy('show', kwargs={'pk':pk})





        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect('/gallery/post/{id}')    



def post_update(request, id):
    post = Post.objects.get(id=id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            # update the existing post in the database
            form.save()
            # redirect to the detail page of the post we just updated
            return redirect('show', post.id)
    else:
        form = PostForm(instance=post)

    return render(request,
                'main_app/post_update.html',
                {'form': form})







@login_required
@method_decorator(login_required, name='dispatch')
def post_update(request, id):
    post = Post.objects.get(id=id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            # update the existing post in the database
            form.save()
            # redirect to the detail page of the post we just updated
            return redirect('show', post.id)
    else:
        form = PostForm(instance=post)

    return render(request,'main_app/post_update.html',{'form': form})                   






@method_decorator(login_required, name='dispatch')
class updatePost(UpdateView):
    model = Post
    fields = ['caption', 'media','category']
    template_name = 'main_app/post_update.html'

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.post = Post.objects.get(pk=id)
        self.object.save()
        return HttpResponseRedirect('/show/' + str(self.object.pk))




        @login_required
def updatePost(request, post_id):
    x = Post.objects.get( id = post_id) # <-- Here
    form = PostForm(request.POST or None, instance=x)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("/gallery")
    return render(request, 'main_app/post_update.html',{'form':form,'post':x})






        <nav aria-label="breadcrumb">
        <ol class="breadcrumb">
            {% if user.is_authenticated %}
            <li class="breadcrumb-item"><a href="/">Home</a></li>
            <li class="breadcrumb-item active" aria-current="page"><a href="/upload">Add Photo</a></li>
            <li class="breadcrumb-item active" aria-current="page"><a href="/gallery">View All Photos</a></li>
            <li class="breadcrumb-item active" aria-current="page"><a href="/user/{{user}}">{{user}}'s Profile</a></li>
            <li class="breadcrumb-item active" aria-current="page"><a href="{% url 'settings' %}">Settings</a></li>
            <li class="breadcrumb-item active" aria-current="page"><a href="{% url 'logout' %}">Logout</a></li>
        {% else %}
            <li class="breadcrumb-item active" aria-current="page"><a href="{% url 'login' %}">Login</a></li>
            <li class="breadcrumb-item active" aria-current="page"><a href="{% url 'signup' %}">Signup</a></li>
        {% endif %}
        </ol>
    </nav>
