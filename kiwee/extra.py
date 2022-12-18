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
