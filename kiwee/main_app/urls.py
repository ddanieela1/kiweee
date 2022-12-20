from django.urls import path
from  . import views



urlpatterns = [

    path('', views.index, name='index'),
    path('gallery/', views.gallery, name ='gallery'),
    path('main_app/<int:post_id>/', views.viewMedia, name ='viewMedia'),
    path('upload/', views.upload, name ='upload'),

    path('main_app/<int:pk>/delete', views.deletePost.as_view(), name ='post_delete'),
    path('main_app/<int:pk>/update', views.updatePost.as_view(), name ='post_update'),

    path('signup/', views.signup, name ='signup'),
    path('login/', views.login_view, name ='login'),
    # path('user/<username>/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('settings/', views.settings, name='settings'),
 
]