from django.urls import path
from  . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('homepage/', views.homepage, name ='homepage'),
    path('signup/', views.signup, name ='signup'),
    path('login/', views.login_view, name ='login'),
    path('user/<username>/', views.profile, name='profile'),
     path('logout/', views.logout_view, name='logout'),
]