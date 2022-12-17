from django.urls import path
from  . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('homepage/', views.homepage, name ='homepage'),
    path('gallery/', views.gallery, name ='gallery'),
    path('show/<int:pk>/', views.viewMedia, name ='viewMedia'),
    path('upload/', views.upload, name ='upload'),
    path('signup/', views.signup, name ='signup'),
    path('login/', views.login_view, name ='login'),
    path('user/<username>/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('settings/', views.settings, name='settings'),
 
]