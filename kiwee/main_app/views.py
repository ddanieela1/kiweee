from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'main_app/index.html')

def homepage(request):
    return render(request, 'homepage.html')

def profile(request):
    return render(request, 'profile.html')

    