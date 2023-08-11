from django.shortcuts import render, redirect,get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth. forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserProfile, WorkerProfile, ClientProfile
from django.contrib.auth.views import LoginView


def sign_up(request):
    if request.method =='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, ("Registered Succesfull !!!"))
            
            user, user_profile = form.save()
            login(request, user)
            return redirect('login') 
    else:
        form = SignUpForm()
    return render(request, 'registration.html', {'form': form})
            # if user_type=='worker':
            #     service = form.cleaned_data.get('service')
            #     description = form.cleaned_data.get('description')
            #     price = form.cleaned_data.get('price')
            #     price_per_day = form.cleaned_data.get('price_per_day')
            #     available_time = form.cleaned_data.get('available_time')
            #     WorkerProfile.objects.create(profile=profile, service=service, description=description, price=price, price_per_day=price_per_day, available_time=available_time)
            # else:
            #     ClientProfile.objects.create(profile=profile)
            
# login

def user_login (request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        form = user.userprofile
        user_type = user.userprofile.user_type
        print(user_type)
        if user_type == 'worker':
           
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in succesfully !!')
            return HttpResponseRedirect(reverse('worker_profile', args=[user.userprofile.pk]))
        # return render(request, 'client_profile.html',{'form':form})
                
                # return redirect('worker_profile')

        
        elif user_type == 'customer':
            if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in succesfully !!')
            return HttpResponseRedirect(reverse('client_profile', args=[user.userprofile.pk]))
            

                    # return render(request, 'client_profile.html',{'form':form})
                    # return redirect('client_profile')

            return redirect('client_profile') 
        
        
        # if user is not None:
        #     login(request, user)
        #     return redirect('profile')  # Redirect to home page after successful login
    else:
        # return redirect('/login/')
        form=AuthenticationForm()
        return render(request, 'login.html',{'form':form})

    # if request.method == 'POST':
    #     form = AuthenticationForm( request=request, data = request.POST)
    #     if form.is_valid():
    #         uname = form.cleaned_data['username']
    #         upass = form.cleaned_data['password']
    #         user = request.user
    #         if user.is_authenticated:
    #             user_type = user.userprofile.user_type

           
    #             user= authenticate(username=uname, password = upass)
    #             return render(request, 'profile.html')

    #             return HttpResponseRedirect(reverse('worker_profile', args=[user.userprofile.pk]))

    #             user_type = user.userprofile.user_type
    #             if user_type == 'worker':
    #                 if user is not None:
    #                     login(request, user)
    #                     messages.success(request, 'Logged in succesfully !!')
    #                     return HttpResponseRedirect(reverse('worker_profile', args=[user.userprofile.pk]))
    #             elif user_type == 'client':
    #                 if user is not None:
    #                     login(request, user)
    #                     messages.success(request, 'Logged in succesfully !!')
    #                 return HttpResponseRedirect(reverse('client_profile', args=[user.userprofile.pk]))               
            
    # else:
    #     form=AuthenticationForm()
    # return render(request, 'login.html',{'form':form})



def profile(request):
    return render(request, 'profile.html')

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/login/')

   
def index(request):
    # return render (request, "registration.html")
    return HttpResponse('this is index page ')

def worker_profile(request, pk):
    user_profile = get_object_or_404(UserProfile, pk=pk)
    return render(request, 'worker_profile.html', {'user_profile': user_profile})
    return render(request, 'worker_profile.html')

def client_profile(request, pk):
    user_profile = get_object_or_404(UserProfile, pk=pk)
    return render(request, 'client_profile.html', {'user_profile': user_profile})
    return render(request, 'client_profile.html')

class CustomLoginView(LoginView):
    template_name = 'login.html'
    
    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect('profile_redirect')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sign_up'] = sign_up()
        return context
    
# def profile_redirect(request):
#     user = request.user
#     if user.is_authenticated:
#         user_type = user.userprofile.user_type
#         if user_type == 'worker':
#             return HttpResponseRedirect(reverse('worker_profile', args=[user.userprofile.pk]))
#         elif user_type == 'client':
#             return HttpResponseRedirect(reverse('client_profile', args=[user.userprofile.pk]))
#     return redirect('login')  # Redirect to login if user is not authenticated