from django.shortcuts import render, HttpResponse, redirect
from .forms import SignUpForm
from django.contrib.auth import login
from django.contrib import messages
from .models import UserProfile

# Create your views here.
def sign_up(request):
    if request.method =='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, ("Registered Succesfull !!!"))
            
            user, user_profile = form.save()
            login(request, user)
    else:
        form = SignUpForm()
    return render(request, 'registration.html', {'form': form})


def index(request):
    # return render (request, "registration.html")
    return HttpResponse('this is index page ')

